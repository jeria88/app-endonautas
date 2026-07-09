import json as _json
import logging
import re as _re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from config.ai_client import call_ai

from .data import (
    FRAMEWORKS_AND_TECHNIQUES,
    MARCO_MTC,
    SYSTEM_DIFERENCIACION,
    SYSTEM_PROPUESTA,
    get_all_tecnicas,
)
from .data.anamnesis import (
    MODULO_EMOCIONAL,
    MODULO_GENERAL,
    OBSERVACION,
    PREGUNTAS_BY_ID,
    ROGA_PARIKSHA,
    SISTEMAS,
)
from .data.terapeutica import FASES_14_DIAS, PRINCIPIOS, RED_FLAGS_DERIVACION
from .forms import Paso1Form, Paso5ResultadoForm
from .models import (
    Consulta,
    DiagnosticoPropuesto,
    MarcoEvaluacion,
    PreguntaRespuesta,
    SeleccionTecnica,
    SintomaConfirmado,
    TecnicaEvaluacion,
)
from .scoring import (
    modulos_especificos_para,
    score_diagnosticos,
    sistemas_desde_motivo,
)

logger = logging.getLogger(__name__)


# ─── IA helper (delega en el cliente centralizado) ────────────────────────────

def _call_ai_json(prompt: str, system: str, max_tokens: int = 1500, temperature: float = 0.2) -> dict:
    """
    Llama a call_ai con el modelo clínico y extrae JSON. Devuelve {} si no hay
    API key o si falla — el motor determinista es la base, esto solo refina.
    """
    raw = call_ai(
        [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        timeout=60,
        model=getattr(settings, "AI_MODEL_CLINICO", None),
        temperature=temperature,
        json_mode=True,
    )
    if not raw:
        return {}
    raw = raw.strip()
    for extractor in (
        lambda s: _json.loads(s),
        lambda s: _json.loads(_re.search(r'```(?:json)?\s*(\{.*?\})\s*```', s, _re.DOTALL).group(1)),
        lambda s: _json.loads(_re.search(r'(\{.*\})', s, _re.DOTALL).group(1)),
    ):
        try:
            return extractor(raw)
        except Exception:
            continue
    logger.warning("Terapeuta: sin JSON en respuesta IA: %s", raw[:200])
    return {}


# ─── Anamnesis: parseo y persistencia de signos ───────────────────────────────

def _parse_signos(request: HttpRequest, preguntas: list) -> dict:
    out = {}
    for q in preguntas:
        key = f"signo_{q['id']}"
        if q["tipo"] == "checkbox":
            vals = request.POST.getlist(key)
            if vals:
                out[q["id"]] = vals
        else:
            v = request.POST.get(key, "").strip()
            if v:
                out[q["id"]] = v
    return out


def _merge_signos(consulta: Consulta, nuevos: dict):
    s = dict(consulta.signos or {})
    s.update(nuevos)
    consulta.signos = s


def _etiquetas_signo(qid: str, val) -> str:
    q = PREGUNTAS_BY_ID.get(qid)
    if not q:
        return str(val)
    vals = val if isinstance(val, list) else [val]
    labels = []
    for v in vals:
        opt = next((o for o in q["opciones"] if o["valor"] == v), None)
        labels.append(opt["etiqueta"] if opt else v)
    return ", ".join(labels)


def _preguntas_mostradas(consulta: Consulta) -> list:
    ids = [q["id"] for q in ROGA_PARIKSHA]
    ids += [q["id"] for q in MODULO_GENERAL]
    ids += [q["id"] for q in OBSERVACION]
    ids += [q["id"] for q in MODULO_EMOCIONAL]
    for _sid, _nombre, preguntas in modulos_especificos_para(consulta.sistemas_afectados or []):
        ids += [q["id"] for q in preguntas]
    return ids


# ─── Wizard ───────────────────────────────────────────────────────────────────

def _check_terapeuta_plan(request):
    from accounts.plan_utils import plan_at_least, upgrade_wall
    if not plan_at_least(request.user, 'navegante'):
        return upgrade_wall(request, 'navegante', 'Módulo Terapeuta')
    return None


@login_required
def wizard_paso0(request: HttpRequest) -> HttpResponse:
    wall = _check_terapeuta_plan(request)
    if wall:
        return wall
    consulta = Consulta.objects.create(modo="autoconsulta", paso_actual=1, usuario=request.user)
    return redirect("terapeuta:paso1", consulta_id=consulta.id)


@login_required
def wizard_paso1(request: HttpRequest, consulta_id: int) -> HttpResponse:
    """Motivo + triaje de sistemas + Roga Pariksha (nidana, upashaya) + red flags."""
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == "POST":
        form = Paso1Form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            consulta.nombre_paciente = cd.get("nombre_paciente", "")
            consulta.edad = cd.get("edad")
            consulta.ocupacion = cd.get("ocupacion", "")
            consulta.motivo = cd["motivo"]
            consulta.intensidad = cd.get("intensidad")
            consulta.duracion = cd.get("duracion", "")
            consulta.medicamentos_actuales = cd.get("medicamentos_actuales", "")
            consulta.senales_alarma = bool(cd.get("senales_alarma", []))

            # triaje: sistemas elegidos ∪ derivados de keywords del motivo
            elegidos = [s for s in request.POST.getlist("sistemas") if s in {x["id"] for x in SISTEMAS}]
            derivados = sistemas_desde_motivo(consulta.motivo)
            consulta.sistemas_afectados = list(dict.fromkeys(elegidos + derivados)) or ["otro"]

            # Roga Pariksha
            _merge_signos(consulta, _parse_signos(request, ROGA_PARIKSHA))

            consulta.paso_actual = 2
            if consulta.modo == "autoconsulta" and not consulta.nombre_paciente:
                from django.utils import timezone
                fecha = timezone.now().strftime("%d/%m/%y")
                motivo_short = (consulta.motivo or "")[:40].rstrip()
                if len(consulta.motivo or "") > 40:
                    motivo_short += "…"
                consulta.nombre_paciente = f"{motivo_short} · {fecha}"
            consulta.save()
            return redirect("terapeuta:paso2", consulta_id=consulta.id)
    else:
        form = Paso1Form(initial={
            "nombre_paciente": consulta.nombre_paciente, "edad": consulta.edad,
            "ocupacion": consulta.ocupacion, "motivo": consulta.motivo,
            "intensidad": consulta.intensidad, "duracion": consulta.duracion,
            "medicamentos_actuales": consulta.medicamentos_actuales,
        })
    return render(request, "terapeuta/paso1.html", {
        "form": form, "consulta": consulta, "paso": 1, "total_pasos": 5,
        "sistemas": SISTEMAS, "sistemas_activos": consulta.sistemas_afectados or [],
        "roga": ROGA_PARIKSHA, "signos": consulta.signos or {},
        "cliente": consulta.perfil_cliente,
    })


@login_required
def wizard_paso2(request: HttpRequest, consulta_id: int) -> HttpResponse:
    """Interrogatorio general (Shi Wen)."""
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == "POST":
        _merge_signos(consulta, _parse_signos(request, MODULO_GENERAL))
        consulta.paso_actual = 3
        consulta.save(update_fields=["signos", "paso_actual"])
        return redirect("terapeuta:paso3", consulta_id=consulta.id)
    return render(request, "terapeuta/paso2.html", {
        "consulta": consulta, "preguntas": MODULO_GENERAL, "signos": consulta.signos or {},
        "paso": 2, "total_pasos": 5,
    })


@login_required
def wizard_paso3(request: HttpRequest, consulta_id: int) -> HttpResponse:
    """Auto-observación (lengua, cara, pulso) + módulo específico + contexto emocional."""
    consulta = get_object_or_404(Consulta, id=consulta_id)
    especificos = modulos_especificos_para(consulta.sistemas_afectados or [])
    if request.method == "POST":
        todas = list(OBSERVACION) + list(MODULO_EMOCIONAL)
        for _sid, _nombre, preguntas in especificos:
            todas += preguntas
        _merge_signos(consulta, _parse_signos(request, todas))
        # limpiar diagnósticos previos: se recalculan en paso4 con signos completos
        DiagnosticoPropuesto.objects.filter(consulta=consulta).delete()
        consulta.paso_actual = 4
        consulta.save(update_fields=["signos", "paso_actual"])
        return redirect("terapeuta:paso4", consulta_id=consulta.id)
    return render(request, "terapeuta/paso3.html", {
        "consulta": consulta, "observacion": OBSERVACION, "especificos": especificos,
        "emocional": MODULO_EMOCIONAL, "signos": consulta.signos or {},
        "paso": 3, "total_pasos": 5,
    })


def _escribir_preguntas_respuestas(consulta: Consulta):
    """Dual-write: reconstruye PreguntaRespuesta (texto humano) desde signos."""
    PreguntaRespuesta.objects.filter(consulta=consulta).delete()
    orden = 0
    for qid, val in (consulta.signos or {}).items():
        q = PREGUNTAS_BY_ID.get(qid)
        if not q:
            continue
        PreguntaRespuesta.objects.create(
            consulta=consulta, pregunta=q["pregunta"],
            respuesta=_etiquetas_signo(qid, val), pregunta_id=qid, orden=orden,
        )
        orden += 1


def _refinar_diagnosticos_ia(formula: dict, candidatos: list) -> dict:
    """
    La IA elige 2-4 de los candidatos y justifica cada uno. Devuelve
    {id: justificacion}. Fallback: top-3 con justificación = evidencia a favor.
    """
    fallback = {
        c["id"]: "; ".join(c["a_favor"][:4]) or "Coincide con el patrón de la anamnesis."
        for c in candidatos[:3]
    }
    if not candidatos:
        return {}
    resumen = [
        {"id": c["id"], "titulo": c["titulo"], "marco": c["marco"],
         "confianza": c["confianza"], "a_favor": c["a_favor"], "en_contra": c["en_contra"],
         "patron_diagnostico": (c.get("patron") or {}).get("patron_diagnostico", "")[:400]}
        for c in candidatos
    ]
    prompt = (
        f"Fórmula diagnóstica (MTC): {formula.get('texto', '')}\n"
        + (f"Nota: {formula['contradiccion']}\n" if formula.get("contradiccion") else "")
        + "\nPatrones candidatos (lista cerrada, elige solo de aquí):\n"
        + _json.dumps(resumen, ensure_ascii=False)
        + '\n\nDevuelve JSON: {"seleccionados": [{"id": "M28", "justificacion": "..."}]} '
          "con 2-4 patrones coherentes con la evidencia. La justificación cita signos concretos."
    )
    data = _call_ai_json(prompt, SYSTEM_DIFERENCIACION, max_tokens=1200)
    ids_validos = {c["id"] for c in candidatos}
    elegidos = {}
    for item in (data.get("seleccionados") or []):
        if isinstance(item, dict) and item.get("id") in ids_validos:
            elegidos[item["id"]] = (item.get("justificacion") or "").strip()
    return elegidos or fallback


def _generar_diagnosticos(consulta: Consulta) -> list:
    """Corre el motor, persiste fórmula/ejes, refina con IA y crea los snapshots."""
    resultado = score_diagnosticos(
        consulta.signos or {}, consulta.sistemas_afectados or [],
        _preguntas_mostradas(consulta),
    )
    consulta.ejes_resultado = resultado["ejes"]
    consulta.formula_mtc = resultado["formula"]
    consulta.save(update_fields=["ejes_resultado", "formula_mtc"])

    candidatos = resultado["candidatos"]
    if not candidatos:
        return []
    elegidos = _refinar_diagnosticos_ia(resultado["formula"], candidatos)

    all_tecnicas = {t.codigo_interno: t for t in TecnicaEvaluacion.objects.all()}
    all_marcos = {m.nombre: m for m in MarcoEvaluacion.objects.all()}
    _escribir_preguntas_respuestas(consulta)

    diagnosticos = []
    with transaction.atomic():
        DiagnosticoPropuesto.objects.filter(consulta=consulta).delete()
        # ordenar: los elegidos por IA primero, luego el resto por confianza
        candidatos_ordenados = (
            [c for c in candidatos if c["id"] in elegidos]
            + [c for c in candidatos if c["id"] not in elegidos]
        )
        for idx, c in enumerate(candidatos_ordenados[:4]):
            patron = c.get("patron") or {}
            marco_nombre = c["marco"]
            tecnica_codigo = c["tecnica"]
            diag = DiagnosticoPropuesto.objects.create(
                consulta=consulta,
                titulo=c["titulo"],
                descripcion=patron.get("descripcion", ""),
                etiologia=patron.get("etiologia", ""),
                mecanismo=patron.get("mecanismo", ""),
                patron_diagnostico=patron.get("patron_diagnostico", ""),
                protocolo_indicado=patron.get("protocolo_indicado", ""),
                contraindicaciones=patron.get("contraindicaciones", ""),
                integracion=patron.get("integracion", ""),
                marco_asociado=all_marcos.get(marco_nombre),
                tecnica_asociada=all_tecnicas.get(tecnica_codigo),
                diagnostico_id=c["id"],
                puntaje=c["score"],
                confianza=c["confianza"],
                evidencia={
                    "a_favor": c["a_favor"], "en_contra": c["en_contra"],
                    "justificacion_ia": elegidos.get(c["id"], ""),
                },
                orden=idx,
            )
            for sintoma_texto in patron.get("sintomas", []):
                SintomaConfirmado.objects.create(diagnostico=diag, sintoma_texto=sintoma_texto, presente=True)
            diagnosticos.append(diag)

        # Técnicas se derivan de los diagnósticos (decisión de diseño: el usuario
        # de autoconsulta no elige técnicas manualmente).
        SeleccionTecnica.objects.filter(consulta=consulta).delete()
        for diag in diagnosticos:
            if diag.tecnica_asociada:
                SeleccionTecnica.objects.get_or_create(
                    consulta=consulta, tecnica=diag.tecnica_asociada,
                    defaults={"fue_recomendada_por_sistema": True},
                )
    return diagnosticos


@login_required
def wizard_paso4(request: HttpRequest, consulta_id: int) -> HttpResponse:
    """Síntesis (fórmula) + diagnóstico diferencial con evidencia."""
    consulta = get_object_or_404(Consulta, id=consulta_id)

    if request.method == "POST":
        diagnosticos_ids = request.POST.getlist("diagnosticos_confirmados")
        with transaction.atomic():
            for diag in DiagnosticoPropuesto.objects.filter(consulta=consulta):
                diag.fue_confirmado_por_usuario = str(diag.id) in diagnosticos_ids
                diag.save(update_fields=["fue_confirmado_por_usuario"])
            consulta.paso_actual = 5
            consulta.save(update_fields=["paso_actual"])
        return redirect("terapeuta:paso5", consulta_id=consulta.id)

    diagnosticos = list(
        DiagnosticoPropuesto.objects.filter(consulta=consulta)
        .select_related("marco_asociado", "tecnica_asociada").order_by("orden")
    )
    if not diagnosticos:
        diagnosticos = _generar_diagnosticos(consulta)

    respuestas = PreguntaRespuesta.objects.filter(consulta=consulta).order_by("orden")
    return render(request, "terapeuta/paso4.html", {
        "consulta": consulta, "diagnosticos": diagnosticos,
        "formula": consulta.formula_mtc or {}, "respuestas": respuestas,
        "paso": 4, "total_pasos": 5,
    })


def _principios_desde_formula(formula: dict, ejes: dict) -> list:
    """Deriva los principios de tratamiento (bloques de terapeutica) desde la fórmula."""
    claves = []
    termico = formula.get("termico")
    plenitud = formula.get("plenitud")
    if termico == "Calor":
        claves.append("enfriar")
    elif termico == "Frío":
        claves.append("calentar")
    factores = formula.get("factores", [])
    for f in factores:
        if f.startswith("Humedad") or f.startswith("Mucosidad"):
            claves.append("drenar_humedad")
        if f.startswith("Viento"):
            claves.append("dispersar_viento")
        if f.startswith("Estasis"):
            claves.append("mover_sangre")
        if f.startswith("Estancamiento de Qi"):
            claves.append("mover_qi")
    for s in formula.get("sustancias", []):
        if "Qi" in s:
            claves.append("tonificar_qi")
        if "Sangre" in s:
            claves.append("nutrir_sangre")
        if "Yin" in s:
            claves.append("nutrir_yin")
        if "Yang" in s:
            claves.append("calentar")
    # dedup preservando orden
    vistos, out = set(), []
    for k in claves:
        if k in PRINCIPIOS and k not in vistos:
            vistos.add(k)
            out.append({"clave": k, **PRINCIPIOS[k]})
    return out[:4]


def _generar_propuesta_fallback(consulta: Consulta, diagnosticos: list, principios: list) -> dict:
    plan = []
    for pr in principios:
        plan.append({
            "titulo": pr["titulo"], "icono": "🌿",
            "pasos": [
                {"instruccion": pr["dieta"], "fundamento": pr["cuando"]},
                {"instruccion": pr["acupresion"], "fundamento": "Acupresión con los dedos, sin agujas."},
                {"instruccion": pr["estilo_vida"], "fundamento": ""},
            ],
        })
    titulos = " y ".join(d.titulo for d in diagnosticos[:2]) or "el patrón identificado"
    precauciones = next((d.contraindicaciones for d in diagnosticos if d.contraindicaciones), "")
    return {
        "sintesis": f"La lectura de tus signos apunta a {titulos}. El plan aplica el principio de "
                    f"tratamiento correspondiente mediante autoaplicación durante 14 días.",
        "formula": (consulta.formula_mtc or {}).get("texto", ""),
        "plan": plan,
        "fases": FASES_14_DIAS,
        "precauciones": (precauciones[:400] + " " + RED_FLAGS_DERIVACION).strip(),
    }


def _generar_propuesta_terapeutica(consulta: Consulta, diagnosticos: list) -> dict | None:
    if not diagnosticos:
        return None
    principios = _principios_desde_formula(consulta.formula_mtc or {}, consulta.ejes_resultado or {})
    if not principios:
        # sin principios claros (p.ej. dominan diagnósticos de otros paradigmas)
        principios = [{"clave": "tonificar_qi", **PRINCIPIOS["tonificar_qi"]}]

    bloques = "\n".join(
        f"- {p['titulo']}: dieta={p['dieta']} | acupresión={p['acupresion']} | estilo de vida={p['estilo_vida']}"
        for p in principios
    )
    dx_txt = "\n".join(f"- {d.titulo} (confianza {d.confianza}): {d.patron_diagnostico[:200]}" for d in diagnosticos)
    contexto = f"Motivo: {consulta.motivo}"
    if consulta.intensidad:
        contexto += f" · Intensidad {consulta.intensidad}/10"
    if consulta.duracion:
        contexto += f" · {consulta.get_duracion_display()}"

    prompt = (
        f"{contexto}\n"
        f"Fórmula MTC: {(consulta.formula_mtc or {}).get('texto', '')}\n\n"
        f"Patrones confirmados:\n{dx_txt}\n\n"
        f"Bloques de terapéutica seleccionados por principio (usa SOLO estos):\n{bloques}\n\n"
        "Redacta un plan de autoaplicación de 14 días. Devuelve ÚNICAMENTE JSON:\n"
        '{\n'
        '  "sintesis": "2-3 frases claras de qué está pasando y hacia dónde apunta el tratamiento",\n'
        '  "plan": [\n'
        '    {"titulo": "nombre del bloque", "icono": "emoji",\n'
        '     "pasos": [{"instruccion": "qué hacer, concreto y con frecuencia", "fundamento": "por qué esta técnica para este patrón"}]}\n'
        '  ],\n'
        '  "precauciones": "contraindicaciones y señales de derivación"\n'
        '}\n'
        "Máximo 3 pasos por bloque. Español neutro."
    )
    data = _call_ai_json(prompt, SYSTEM_PROPUESTA, max_tokens=2500, temperature=0.3)
    if data.get("sintesis") and data.get("plan"):
        data.setdefault("fases", FASES_14_DIAS)
        data.setdefault("formula", (consulta.formula_mtc or {}).get("texto", ""))
        data["precauciones"] = (data.get("precauciones", "") + " " + RED_FLAGS_DERIVACION).strip()
        return data
    logger.warning("Terapeuta: propuesta IA incompleta — usando fallback de bloques")
    return _generar_propuesta_fallback(consulta, diagnosticos, principios)


@login_required
def wizard_paso5(request: HttpRequest, consulta_id: int) -> HttpResponse:
    consulta = get_object_or_404(Consulta, id=consulta_id)
    diagnosticos_confirmados = DiagnosticoPropuesto.objects.filter(
        consulta=consulta, fue_confirmado_por_usuario=True
    ).select_related("marco_asociado", "tecnica_asociada")
    if not diagnosticos_confirmados.exists():
        diagnosticos_confirmados = DiagnosticoPropuesto.objects.filter(
            consulta=consulta
        ).select_related("marco_asociado", "tecnica_asociada")

    if request.method == "POST":
        if request.POST.get("accion") == "regenerar":
            consulta.propuesta_terapeutica = ""
            consulta.save(update_fields=["propuesta_terapeutica"])
            return redirect("terapeuta:paso5", consulta_id=consulta.id)
        form = Paso5ResultadoForm(request.POST)
        if form.is_valid():
            consulta.diagnostico_final = form.cleaned_data.get("diagnostico_final", "")
            consulta.paso_actual = 5
            consulta.save(update_fields=["diagnostico_final", "paso_actual"])
            messages.success(request, "Consulta guardada.")
            return redirect("terapeuta:detalle", consulta_id=consulta.id)
    else:
        form = Paso5ResultadoForm(initial={"diagnostico_final": consulta.diagnostico_final})

    propuesta = None
    propuesta_error = False
    if consulta.propuesta_terapeutica:
        try:
            propuesta = _json.loads(consulta.propuesta_terapeutica)
        except _json.JSONDecodeError:
            propuesta = None

    if propuesta is None and diagnosticos_confirmados.exists():
        propuesta = _generar_propuesta_terapeutica(consulta, list(diagnosticos_confirmados))
        if propuesta:
            consulta.propuesta_terapeutica = _json.dumps(propuesta, ensure_ascii=False)
            consulta.save(update_fields=["propuesta_terapeutica"])
        else:
            propuesta_error = True

    selecciones = SeleccionTecnica.objects.filter(consulta=consulta).select_related("tecnica", "tecnica__marco")
    return render(request, "terapeuta/paso5.html", {
        "consulta": consulta, "form": form,
        "diagnosticos_confirmados": diagnosticos_confirmados,
        "formula": consulta.formula_mtc or {},
        "selecciones": selecciones, "propuesta": propuesta,
        "propuesta_error": propuesta_error, "paso": 5, "total_pasos": 5,
    })


@login_required
def consulta_detalle(request: HttpRequest, consulta_id: int) -> HttpResponse:
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == "POST":
        accion = request.POST.get("accion", "")
        if accion == "regenerar_propuesta":
            consulta.propuesta_terapeutica = ""
            consulta.save(update_fields=["propuesta_terapeutica"])
            return redirect("terapeuta:paso5", consulta_id=consulta.id)
        if accion == "guardar_notas":
            consulta.diagnostico_final = request.POST.get("diagnostico_final", "")
            consulta.save(update_fields=["diagnostico_final"])
            messages.success(request, "Notas guardadas.")
            return redirect("terapeuta:detalle", consulta_id=consulta.id)
        if accion == "editar_basicos":
            consulta.nombre_paciente = request.POST.get("nombre_paciente", "").strip()
            edad = request.POST.get("edad", "")
            consulta.edad = int(edad) if edad.isdigit() else None
            motivo = request.POST.get("motivo", "").strip()
            if motivo:
                consulta.motivo = motivo
            consulta.diagnostico_final = request.POST.get("diagnostico_final", "").strip()
            consulta.save(update_fields=["nombre_paciente", "edad", "motivo", "diagnostico_final"])
            messages.success(request, "Cambios guardados.")
            return redirect("terapeuta:detalle", consulta_id=consulta.id)

    selecciones = SeleccionTecnica.objects.filter(consulta=consulta).select_related("tecnica", "tecnica__marco")
    preguntas = PreguntaRespuesta.objects.filter(consulta=consulta).order_by("orden")
    diagnosticos = DiagnosticoPropuesto.objects.filter(consulta=consulta).select_related("marco_asociado", "tecnica_asociada").order_by("orden")
    propuesta = None
    if consulta.propuesta_terapeutica:
        try:
            propuesta = _json.loads(consulta.propuesta_terapeutica)
        except _json.JSONDecodeError:
            pass

    return render(request, "terapeuta/detalle.html", {
        "consulta": consulta, "selecciones": selecciones, "preguntas": preguntas,
        "diagnosticos": diagnosticos, "formula": consulta.formula_mtc or {},
        "diagnosticos_confirmados": [d for d in diagnosticos if d.fue_confirmado_por_usuario],
        "propuesta": propuesta,
        "perfil_cliente": consulta.perfil_cliente,
    })


@login_required
def consulta_eliminar(request: HttpRequest, consulta_id: int) -> HttpResponse:
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == "POST":
        consulta.delete()
        messages.success(request, "Consulta eliminada.")
        return redirect("terapeuta:lista")
    return render(request, "terapeuta/confirmar_eliminar.html", {"consulta": consulta})


@login_required
def consulta_lista(request: HttpRequest) -> HttpResponse:
    from django.db.models import Count, Q
    qs = Consulta.objects.all()
    if request.user.is_authenticated:
        qs = qs.filter(usuario=request.user)
    consultas = qs.annotate(
        n_diagnosticos=Count("diagnosticos"),
        n_confirmados=Count("diagnosticos", filter=Q(diagnosticos__fue_confirmado_por_usuario=True)),
    ).order_by("-fecha_creacion")[:50]
    return render(request, "terapeuta/lista.html", {"consultas": consultas})
