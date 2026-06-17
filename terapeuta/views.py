import json as _json
import logging
import re as _re

import requests as _requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .constants import (
    AI_SYSTEM_PROMPT,
    DIAGNOSIS_CATALOG,
    FRAMEWORKS_AND_TECHNIQUES,
    KEYWORD_TO_FRAMEWORKS,
    QUESTIONS_BANK,
    get_all_tecnicas,
    get_tecnica_to_framework_map,
)
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

logger = logging.getLogger(__name__)

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# ─── OpenRouter helper ────────────────────────────────────────────────────────

def _call_ai_json(prompt: str, system: str = "", max_tokens: int = 2000, temperature: float = 0.1, max_retries: int = 2, model: str | None = None) -> dict:
    api_key = getattr(settings, "OPENROUTER_API_KEY", "")
    if not api_key:
        return {}
    _model = model or getattr(settings, "OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
    sys_msg = system or AI_SYSTEM_PROMPT

    for attempt in range(max_retries):
        try:
            payload: dict = {
                "model": _model,
                "messages": [
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            # json_object mode solo para modelos que lo soportan
            if _model in ("openrouter/auto",) or any(x in _model for x in ("gpt-4", "claude", "gemini")):
                payload["response_format"] = {"type": "json_object"}
            resp = _requests.post(
                _OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json; charset=utf-8",
                    "HTTP-Referer": "https://endonautas.cl",
                    "X-Title": "Endonautas",
                },
                data=_json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                timeout=60,
            )
            resp.raise_for_status()
            raw = resp.json()["choices"][0]["message"]["content"].strip()
            try:
                return _json.loads(raw)
            except _json.JSONDecodeError:
                pass
            m = _re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw, _re.DOTALL)
            if m:
                return _json.loads(m.group(1))
            m = _re.search(r'(\{.*\})', raw, _re.DOTALL)
            if m:
                return _json.loads(m.group(1))
            logger.warning(f"No JSON found in AI response (attempt {attempt + 1}): {raw[:200]}")
        except (_json.JSONDecodeError, KeyError, IndexError) as e:
            logger.warning(f"AI JSON parse error (attempt {attempt + 1}): {e}")
        except Exception as e:
            logger.error(f"AI call failed: {e}")
            break
    return {}


# ─── Validation helpers ───────────────────────────────────────────────────────

def _validate_ai_recomendacion_tecnicas(data: dict) -> list[dict]:
    results = []
    items = data.get("tecnicas_recomendadas", [])
    if not isinstance(items, list):
        return results
    valid_tecnicas = get_all_tecnicas()
    valid_frameworks = set(FRAMEWORKS_AND_TECHNIQUES.keys())
    tecnica_map = get_tecnica_to_framework_map()
    for item in items:
        marco = item.get("marco", "")
        tecnica = item.get("tecnica", "")
        if marco in valid_frameworks and tecnica in valid_tecnicas and tecnica_map.get(tecnica) == marco:
            results.append({"marco": marco, "tecnica": tecnica})
    return results


def _validate_ai_preguntas(data: dict) -> list[str]:
    valid_ids = {q["id"] for q in QUESTIONS_BANK}
    items = data.get("preguntas_seleccionadas", [])
    return [qid for qid in (items if isinstance(items, list) else []) if qid in valid_ids]


def _validate_ai_diagnosticos(data: dict) -> list[str]:
    valid_ids = {d["id"] for d in DIAGNOSIS_CATALOG}
    items = data.get("diagnosticos_seleccionados", [])
    return [did for did in (items if isinstance(items, list) else []) if did in valid_ids]


# ─── Keyword-based recommendation ─────────────────────────────────────────────

def recomendar_frameworks_por_keywords(motivo: str) -> list[str]:
    motivo_lower = motivo.lower()
    frameworks_recomendados = set()
    for keyword, frameworks in KEYWORD_TO_FRAMEWORKS.items():
        if keyword in motivo_lower:
            frameworks_recomendados.update(frameworks)
    if not frameworks_recomendados:
        return list(FRAMEWORKS_AND_TECHNIQUES.keys())
    return list(frameworks_recomendados)


# ─── Wizard views ─────────────────────────────────────────────────────────────

@login_required
def wizard_paso0(request: HttpRequest) -> HttpResponse:
    consulta = Consulta.objects.create(modo="autoconsulta", paso_actual=1, usuario=request.user)
    return redirect("terapeuta:paso1", consulta_id=consulta.id)


@login_required
def wizard_paso1(request: HttpRequest, consulta_id: int) -> HttpResponse:
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
            alarmas = cd.get("senales_alarma", [])
            consulta.senales_alarma = bool(alarmas)
            consulta.paso_actual = 2
            consulta.save()
            return redirect("terapeuta:paso2", consulta_id=consulta.id)
    else:
        form = Paso1Form(initial={
            "nombre_paciente": consulta.nombre_paciente, "edad": consulta.edad,
            "ocupacion": consulta.ocupacion, "motivo": consulta.motivo,
            "intensidad": consulta.intensidad, "duracion": consulta.duracion,
            "medicamentos_actuales": consulta.medicamentos_actuales,
        })
    return render(request, "terapeuta/paso1.html", {"form": form, "consulta": consulta, "paso": 1, "total_pasos": 5})


@login_required
def wizard_paso2(request: HttpRequest, consulta_id: int) -> HttpResponse:
    consulta = get_object_or_404(Consulta, id=consulta_id)
    texto_completo = consulta.motivo + (" " + consulta.medicamentos_actuales if consulta.medicamentos_actuales else "")
    marcos_recomendados = recomendar_frameworks_por_keywords(texto_completo)
    consulta.marcos_recomendados = marcos_recomendados
    consulta.save(update_fields=["marcos_recomendados"])

    marcos_data = []
    for marco_name, marco_info in FRAMEWORKS_AND_TECHNIQUES.items():
        es_recomendado = marco_name in marcos_recomendados
        tecnicas_list = [
            {"codigo": tec_code, "nombre": tec_info["nombre"], "descripcion": tec_info["descripcion"], "preseleccionada": es_recomendado}
            for tec_code, tec_info in marco_info["tecnicas"].items()
        ]
        marcos_data.append({
            "nombre": marco_name, "descripcion": marco_info["descripcion"],
            "framework_code": marco_info["framework_code"],
            "es_recomendado": es_recomendado, "tecnicas": tecnicas_list,
        })

    if request.method == "POST":
        tecnicas_seleccionadas = request.POST.getlist("tecnicas")
        if not tecnicas_seleccionadas:
            messages.error(request, "Debes seleccionar al menos una técnica.")
        else:
            all_tecnicas = get_all_tecnicas()
            valid_codes = set(all_tecnicas.keys())
            tecnicas_seleccionadas = [t for t in tecnicas_seleccionadas if t in valid_codes]
            with transaction.atomic():
                SeleccionTecnica.objects.filter(consulta=consulta).delete()
                for tec_code in tecnicas_seleccionadas:
                    tecnica_obj = TecnicaEvaluacion.objects.get(codigo_interno=tec_code)
                    fue_recomendado = tec_code in [
                        t["codigo"] for m in marcos_data if m["es_recomendado"] for t in m["tecnicas"]
                    ]
                    SeleccionTecnica.objects.create(consulta=consulta, tecnica=tecnica_obj, fue_recomendada_por_sistema=fue_recomendado)
                consulta.paso_actual = 3
                consulta.save(update_fields=["paso_actual"])
            return redirect("terapeuta:paso3", consulta_id=consulta.id)

    return render(request, "terapeuta/paso2.html", {"consulta": consulta, "marcos_data": marcos_data, "paso": 2, "total_pasos": 5})


@login_required
def wizard_paso3(request: HttpRequest, consulta_id: int) -> HttpResponse:
    consulta = get_object_or_404(Consulta, id=consulta_id)
    selecciones = SeleccionTecnica.objects.filter(consulta=consulta).select_related("tecnica")
    tecnicas_codigos = [s.tecnica.codigo_interno for s in selecciones]
    if not tecnicas_codigos:
        messages.warning(request, "No hay técnicas seleccionadas. Volviendo al paso 2.")
        return redirect("terapeuta:paso2", consulta_id=consulta.id)

    if request.method == "POST":
        with transaction.atomic():
            PreguntaRespuesta.objects.filter(consulta=consulta).delete()
            for key, value in request.POST.items():
                if not key.startswith("respuesta_"):
                    continue
                suffix = key[len("respuesta_"):]
                if suffix.startswith("radio_") or suffix.startswith("cb_") or suffix.startswith("otro_"):
                    continue
                pregunta_id = suffix
                pregunta_texto = request.POST.get(f"pregunta_texto_{pregunta_id}", "")
                tecnica_codigo = request.POST.get(f"pregunta_tecnica_{pregunta_id}", "")
                respuesta = value.strip()
                if not respuesta:
                    continue
                tecnica_obj = None
                if tecnica_codigo:
                    try:
                        tecnica_obj = TecnicaEvaluacion.objects.get(codigo_interno=tecnica_codigo)
                    except TecnicaEvaluacion.DoesNotExist:
                        pass
                try:
                    orden = int(pregunta_id.replace("Q", "").replace("q", ""))
                except ValueError:
                    orden = 0
                PreguntaRespuesta.objects.create(
                    consulta=consulta, pregunta=pregunta_texto, respuesta=respuesta,
                    tecnica_asociada=tecnica_obj, pregunta_id=pregunta_id, orden=orden,
                )
            consulta.paso_actual = 4
            consulta.save(update_fields=["paso_actual"])
        return redirect("terapeuta:paso4", consulta_id=consulta.id)

    preguntas = _seleccionar_preguntas_ia(consulta, tecnicas_codigos)
    return render(request, "terapeuta/paso3.html", {"consulta": consulta, "preguntas": preguntas, "tecnicas_seleccionadas": tecnicas_codigos, "paso": 3, "total_pasos": 5})


def _seleccionar_preguntas_ia(consulta: Consulta, tecnicas_codigos: list) -> list:
    banco_json = _json.dumps(QUESTIONS_BANK, ensure_ascii=False)
    contexto_extra = ""
    if consulta.intensidad:
        contexto_extra += f"\nIntensidad: {consulta.intensidad}/10"
    if consulta.duracion:
        contexto_extra += f"\nDuración: {consulta.duracion}"
    if consulta.medicamentos_actuales:
        contexto_extra += f"\nMedicamentos: {consulta.medicamentos_actuales}"

    prompt = f"""Motivo de consulta: {consulta.motivo}{contexto_extra}

Técnicas seleccionadas: {_json.dumps(tecnicas_codigos, ensure_ascii=False)}

Banco de preguntas:
{banco_json}

Selecciona 8-12 preguntas relevantes. Devuelve JSON: {{"preguntas_seleccionadas": ["Q01", "Q03", ...]}}"""

    ai_response = _call_ai_json(prompt)
    pregunta_ids = _validate_ai_preguntas(ai_response)
    if not pregunta_ids:
        pregunta_ids = _seleccion_determinista_preguntas(tecnicas_codigos)
    return [q for q in QUESTIONS_BANK if q["id"] in pregunta_ids]


def _seleccion_determinista_preguntas(tecnicas_codigos: list) -> list:
    selected = []
    for q in QUESTIONS_BANK:
        if len(set(q["tecnicas_asociadas"]) & set(tecnicas_codigos)) >= 2:
            selected.append(q["id"])
    for q in QUESTIONS_BANK:
        if q["id"] not in selected and set(q["tecnicas_asociadas"]) & set(tecnicas_codigos):
            selected.append(q["id"])
    return selected[:12]


@login_required
def wizard_paso4(request: HttpRequest, consulta_id: int) -> HttpResponse:
    consulta = get_object_or_404(Consulta, id=consulta_id)
    selecciones = SeleccionTecnica.objects.filter(consulta=consulta).select_related("tecnica")
    tecnicas_codigos = [s.tecnica.codigo_interno for s in selecciones]
    if not tecnicas_codigos:
        return redirect("terapeuta:paso2", consulta_id=consulta.id)
    respuestas = PreguntaRespuesta.objects.filter(consulta=consulta).order_by("orden")

    if request.method == "POST":
        diagnosticos_ids = request.POST.getlist("diagnosticos_confirmados")
        with transaction.atomic():
            for diag in DiagnosticoPropuesto.objects.filter(consulta=consulta):
                diag.fue_confirmado_por_usuario = str(diag.id) in diagnosticos_ids
                diag.save(update_fields=["fue_confirmado_por_usuario"])
            consulta.paso_actual = 5
            consulta.save(update_fields=["paso_actual"])
        return redirect("terapeuta:paso5", consulta_id=consulta.id)

    # Solo generar si no existen aún — evita borrar confirmaciones al volver desde paso5
    diagnosticos = list(
        DiagnosticoPropuesto.objects.filter(consulta=consulta)
        .select_related("marco_asociado", "tecnica_asociada")
        .order_by("orden")
    )
    if not diagnosticos:
        diagnosticos = _seleccionar_diagnosticos_ia(consulta, tecnicas_codigos, respuestas)

    return render(request, "terapeuta/paso4.html", {
        "consulta": consulta, "diagnosticos": diagnosticos,
        "respuestas": respuestas, "paso": 4, "total_pasos": 5,
    })


def _seleccionar_diagnosticos_ia(consulta: Consulta, tecnicas_codigos: list, respuestas) -> list:
    respuestas_texto = "\n".join(f"- {pr.pregunta}: {pr.respuesta}" for pr in respuestas)
    prompt = f"""Motivo: {consulta.motivo}
Técnicas: {_json.dumps(tecnicas_codigos, ensure_ascii=False)}

Respuestas del paciente:
{respuestas_texto}

Catálogo: {_json.dumps(DIAGNOSIS_CATALOG, ensure_ascii=False)}

Selecciona 2-4 diagnósticos. Devuelve JSON: {{"diagnosticos_seleccionados": ["D01", ...]}}"""

    ai_response = _call_ai_json(prompt, max_tokens=1500)
    diagnostico_ids = _validate_ai_diagnosticos(ai_response)
    if not diagnostico_ids:
        diagnostico_ids = _seleccion_determinista_diagnosticos(tecnicas_codigos)

    all_tecnicas = {t.codigo_interno: t for t in TecnicaEvaluacion.objects.all()}
    all_marcos = {m.nombre: m for m in MarcoEvaluacion.objects.all()}
    diagnosticos = []
    with transaction.atomic():
        DiagnosticoPropuesto.objects.filter(consulta=consulta).delete()
        for idx, diag_id in enumerate(diagnostico_ids[:4]):
            entry = next((d for d in DIAGNOSIS_CATALOG if d["id"] == diag_id), None)
            if not entry:
                continue
            diag = DiagnosticoPropuesto.objects.create(
                consulta=consulta, titulo=entry["titulo"], descripcion=entry["descripcion"],
                etiologia=entry.get("etiologia", ""), mecanismo=entry.get("mecanismo", ""),
                patron_diagnostico=entry.get("patron_diagnostico", ""),
                protocolo_indicado=entry.get("protocolo_indicado", ""),
                contraindicaciones=entry.get("contraindicaciones", ""),
                integracion=entry.get("integracion", ""),
                marco_asociado=all_marcos.get(entry["marco_asociado"]),
                tecnica_asociada=all_tecnicas.get(entry["tecnica_asociada"]),
                diagnostico_id=diag_id, orden=idx,
            )
            for sintoma_texto in entry.get("sintomas", []):
                SintomaConfirmado.objects.create(diagnostico=diag, sintoma_texto=sintoma_texto, presente=True)
            diagnosticos.append(diag)
    return diagnosticos


def _seleccion_determinista_diagnosticos(tecnicas_codigos: list) -> list:
    selected = [d["id"] for d in DIAGNOSIS_CATALOG if d["tecnica_asociada"] in tecnicas_codigos]
    tecnicas_cubiertas, diversificados = set(), []
    for did in selected:
        entry = next((d for d in DIAGNOSIS_CATALOG if d["id"] == did), None)
        if entry and entry["tecnica_asociada"] not in tecnicas_cubiertas:
            diversificados.append(did)
            tecnicas_cubiertas.add(entry["tecnica_asociada"])
    for did in selected:
        if did not in diversificados and len(diversificados) < 4:
            diversificados.append(did)
    return diversificados[:4]


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
        "selecciones": selecciones, "propuesta": propuesta,
        "propuesta_error": propuesta_error, "paso": 5, "total_pasos": 5,
    })


_SYSTEM_PROPUESTA = (
    "Eres un terapeuta en salud integrativa. Tu trabajo es leer protocolos clínicos ya definidos "
    "y estructurarlos en lenguaje comprensible. NO inventas protocolos. Respondes siempre con JSON válido."
)

def _generar_propuesta_fallback(diagnosticos: list) -> dict:
    plan = []
    for d in diagnosticos:
        marco = d.marco_asociado.nombre if d.marco_asociado else "Sin marco"
        tecnica = d.tecnica_asociada.nombre if d.tecnica_asociada else "Sin técnica"
        pasos = [d.descripcion] if d.descripcion else []
        if d.protocolo_indicado:
            # Limpiar citas entre paréntesis y tomar primera instrucción concreta
            clean = _re.sub(r'\(ref\.[^)]*\)', '', d.protocolo_indicado).strip()
            clean = _re.sub(r'\s+', ' ', clean)
            # Tomar el texto después del primer punto, si hay sección con ":"
            after = clean.split(':', 1)[1].strip() if ':' in clean else clean
            # Primer fragmento antes de punto y seguido de mayúscula
            m = _re.search(r'^(.{40,250}?)(?:\.\s+[A-ZÁÉÍÓÚ]|\.$)', after, _re.DOTALL)
            if m:
                pasos.append(m.group(1).strip() + '.')
            else:
                pasos.append(after[:220] + '…')
        pasos = [p for p in pasos if p][:2]
        if not pasos:
            pasos = [f"Consultar con profesional certificado en {tecnica}."]
        precauciones_d = (d.contraindicaciones or "").split('.')[0].strip()
        plan.append({
            "marco": marco, "tecnica": tecnica, "diagnostico": d.titulo,
            "icono": "🌿", "pasos": pasos,
            "duracion": "4-6 semanas", "frecuencia": "2-3 sesiones/semana",
            "como_empezar": f"Agendar evaluación con profesional en {tecnica}." + (f" Precaución: {precauciones_d}." if precauciones_d else ""),
        })
    titulos = " y ".join(d.titulo for d in diagnosticos[:2])
    precauciones = next((d.contraindicaciones for d in diagnosticos if d.contraindicaciones), "Consultar con médico si los síntomas empeoran.")
    return {
        "sintesis": f"El análisis identifica patrones de {titulos}. El plan integra las técnicas evaluadas para abordar el caso de forma holística y progresiva.",
        "plan": plan,
        "fases": [
            {"nombre": "Exploración inicial", "duracion": "Semanas 1-2", "objetivo": "Evaluación y primeras intervenciones"},
            {"nombre": "Tratamiento activo", "duracion": "Semanas 3-8", "objetivo": "Implementar el protocolo completo"},
            {"nombre": "Consolidación", "duracion": "Semanas 9-12", "objetivo": "Integrar cambios y prevenir recaídas"},
        ],
        "indicadores": ["Mejora subjetiva del bienestar general", "Reducción de la intensidad del síntoma principal", "Mayor claridad mental y energía sostenida"],
        "precauciones": precauciones[:400],
    }


def _generar_propuesta_terapeutica(consulta: Consulta, diagnosticos: list) -> dict | None:
    if not diagnosticos:
        return None
    bloques = []
    for d in diagnosticos:
        marco = d.marco_asociado.nombre if d.marco_asociado else "Sin marco"
        tecnica = d.tecnica_asociada.nombre if d.tecnica_asociada else "Sin técnica"
        bloques.append(f"""Diagnóstico: {d.titulo}
Marco: {marco} — Técnica: {tecnica}
Descripción: {d.descripcion}
Protocolo indicado: {d.protocolo_indicado or '(no especificado)'}
Integración con otros marcos: {d.integracion or '(no especificado)'}
Contraindicaciones: {d.contraindicaciones or 'ninguna registrada'}""")

    contexto = f"Motivo de consulta: {consulta.motivo}"
    if consulta.intensidad:
        contexto += f"\nIntensidad: {consulta.intensidad}/10"
    if consulta.duracion:
        mapa = {"agudo": "agudo (<2 sem)", "subagudo": "subagudo (2-6 sem)", "cronico": "crónico (>6 sem)"}
        contexto += f"\nDuración: {mapa.get(consulta.duracion, consulta.duracion)}"
    if consulta.medicamentos_actuales:
        contexto += f"\nMedicamentos/terapias actuales: {consulta.medicamentos_actuales}"

    prompt = f"""{contexto}

DIAGNÓSTICOS CONFIRMADOS:

{chr(10).join('---' + chr(10) + b for b in bloques)}

INSTRUCCIÓN CRÍTICA:
El campo "Protocolo indicado" ya contiene el tratamiento clínico específico. Tu trabajo es:
1. Leer el "Protocolo indicado" de cada diagnóstico.
2. Seleccionar los 2-3 pasos más relevantes para ESTE caso.
3. Reformular cada paso en lenguaje directo, conservando nombres específicos (hierbas, puntos, ejercicios, dosis).

Instrucciones por tipo de técnica en el campo "pasos":
— ACUPUNTURA: nombre completo del punto + ubicación anatómica corporal (NO códigos). Añade instrucción de auto-estimulación en casa. Ej: "Punto Tai Chong (Hígado): dorso del pie, entre el 1° y 2° metatarsiano. En consulta: agujas en sedación. En casa: presiona con el pulgar en círculos, firmeza media, 60 segundos, 3 veces/día."
— EJERCICIO/FISIOTERAPIA: nombre + posición inicial → movimiento → respiración → repeticiones. Ej: "Bird-Dog: en cuadrupedia, espalda neutral. Exhala y extiende brazo derecho + pierna izquierda, mantén 3 seg. 3 series × 8 reps cada lado, días alternos."
— FITOTERAPIA: nombre de la hierba, dosis exacta y preparación. Ej: "Ashwagandha KSM-66: 600mg en cápsula con leche tibia, 1 vez al acostarse."
— DIETA: alimentos específicos, cuándo y en qué cantidad.

Devuelve ÚNICAMENTE JSON válido con esta estructura:
{{
  "sintesis": "2-3 oraciones en lenguaje claro que expliquen qué está pasando",
  "plan": [
    {{
      "marco": "nombre del marco",
      "tecnica": "nombre de la técnica",
      "diagnostico": "título del diagnóstico",
      "icono": "emoji representativo",
      "pasos": ["paso detallado 1", "paso detallado 2"],
      "duracion": "tiempo total estimado",
      "frecuencia": "frecuencia específica",
      "como_empezar": "qué hacer exactamente en los primeros 3 días"
    }}
  ],
  "fases": [{{"nombre": "fase", "duracion": "Semanas X-Y", "objetivo": "objetivo medible"}}],
  "indicadores": ["señal concreta observable sin instrumentos"],
  "precauciones": "precauciones concretas de los diagnósticos"
}}

Máximo 3 pasos por disciplina. Responde en español."""

    model_propuesta = getattr(settings, "OPENROUTER_MODEL_PROPUESTA",
                              getattr(settings, "OPENROUTER_MODEL", "openrouter/auto"))
    data = _call_ai_json(prompt, system=_SYSTEM_PROPUESTA, max_tokens=4000, temperature=0.2,
                         model=model_propuesta)
    if data.get("sintesis") and data.get("plan"):
        return data
    logger.warning("Propuesta IA incompleta — usando fallback de catálogo")
    return _generar_propuesta_fallback(diagnosticos)


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
        "diagnosticos": diagnosticos,
        "diagnosticos_confirmados": [d for d in diagnosticos if d.fue_confirmado_por_usuario],
        "propuesta": propuesta,
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
