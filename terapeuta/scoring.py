"""
Motor de diferenciación diagnóstica (determinista).

Dos etapas (ver plan del rediseño):
  A. Acumular ejes desde los signos recolectados en la anamnesis.
  B. Sintetizar la fórmula MTC (ejes.sintetizar_formula) y hacer match de los
     ejes contra las firmas de patrones_mtc.PATRONES_MTC, produciendo candidatos
     con score, confianza y evidencia a favor / en contra.

Los diagnósticos de otros paradigmas (PSI/SOC/VIB/BIO en catalogo_otros) se
puntúan por pesos directos `dx` de las opciones y se integran como candidatos
secundarios.

La IA (en views) solo REFINA sobre estos candidatos; nunca es el único juez.
Si la IA falla, `score_diagnosticos` basta para diagnosticar.
"""
from collections import defaultdict

from .data.anamnesis import (
    MODULOS_ESPECIFICOS,
    PREGUNTAS_BY_ID,
    SISTEMAS,
    SISTEMAS_BY_ID,
)
from .data.catalogo_otros import DIAGNOSIS_OTROS
from .data.ejes import eje_label, sintetizar_formula
from .data.patrones_mtc import MARCO_MTC, PATRONES_MTC

_OTROS_BY_ID = {d["id"]: d for d in DIAGNOSIS_OTROS}

# Constantes del scoring
_CLARITY = 2.0        # magnitud de eje que ya cuenta como "señal clara" (crédito pleno)
_OTROS_CONF_DIV = 6.0  # score de dx directo que equivale a confianza 1.0
_MIN_CONF_MTC = 0.20
_MIN_CONF_OTROS = 0.25
_MAX_POR_MARCO = 2
_TOP_N = 6


# ─────────────────────────────────────────────────────────────
# Triaje: motivo → sistemas
# ─────────────────────────────────────────────────────────────
def sistemas_desde_motivo(texto: str) -> list:
    """Preselecciona ids de sistema cuyas keywords aparecen en el motivo."""
    t = (texto or "").lower()
    encontrados = []
    for s in SISTEMAS:
        if s["id"] == "otro":
            continue
        if any(kw in t for kw in s["keywords"]):
            encontrados.append(s["id"])
    return encontrados


def modulos_especificos_para(sistemas: list) -> list:
    """
    Devuelve [(sistema_id, nombre, [preguntas]), ...] para los sistemas elegidos
    que tienen módulo específico implementado.
    """
    out = []
    for sid in sistemas or []:
        preguntas = MODULOS_ESPECIFICOS.get(sid)
        if preguntas:
            out.append((sid, SISTEMAS_BY_ID.get(sid, {}).get("nombre", sid), preguntas))
    return out


# ─────────────────────────────────────────────────────────────
# Etapa A — acumular ejes y pesos dx desde los signos
# ─────────────────────────────────────────────────────────────
def acumular_ejes(signos: dict, preguntas_mostradas=None):
    """
    signos: {pregunta_id: valor}  (valor = str para radio, list para checkbox)
    preguntas_mostradas: ids de preguntas efectivamente mostradas (para calcular
        una confianza honesta sobre lo que se preguntó). Si None, se usan las
        preguntas presentes en `signos`.

    Devuelve: (ejes: dict, dx: dict, axes_preguntados: set, dx_contrib: dict)
    """
    ejes = defaultdict(float)
    dx = defaultdict(float)
    dx_contrib = defaultdict(list)
    axes_preguntados = set()

    ids_mostradas = list(preguntas_mostradas) if preguntas_mostradas else list(signos.keys())
    for qid in ids_mostradas:
        q = PREGUNTAS_BY_ID.get(qid)
        if not q:
            continue
        for opt in q["opciones"]:
            axes_preguntados.update(opt.get("ejes", {}).keys())

    for qid, val in signos.items():
        q = PREGUNTAS_BY_ID.get(qid)
        if not q:
            continue
        vals = val if isinstance(val, list) else [val]
        for v in vals:
            opt = next((o for o in q["opciones"] if o["valor"] == v), None)
            if not opt:
                continue
            for ax, w in opt.get("ejes", {}).items():
                ejes[ax] += w
            for did, w in opt.get("dx", {}).items():
                dx[did] += w
                if w > 0:
                    dx_contrib[did].append(opt["etiqueta"])

    return dict(ejes), dict(dx), axes_preguntados, dict(dx_contrib)


# ─────────────────────────────────────────────────────────────
# Etapa B — match de firmas MTC
# ─────────────────────────────────────────────────────────────
def _score_firma(firma: dict, ejes: dict, axes_preguntados: set):
    score = 0.0
    max_pos = 0.0
    a_favor, en_contra = [], []
    for ax, target in firma.items():
        w = abs(target)
        target_pos = target > 0
        if ax in axes_preguntados:
            max_pos += w
        o = ejes.get(ax, 0)
        if o == 0:
            continue
        strength = min(1.0, abs(o) / _CLARITY)
        if (o > 0) == target_pos:
            score += w * strength
            a_favor.append(eje_label(ax, target_pos))
        else:
            score -= w * strength
            en_contra.append(eje_label(ax, o > 0))
    conf = max(0.0, score) / max_pos if max_pos > 0 else 0.0
    return score, conf, a_favor, en_contra


def _firma_elegible(patron: dict, sistemas: list) -> bool:
    sis = patron.get("sistemas", [])
    if "general" in sis:
        return True
    if not sistemas:
        return True
    return bool(set(sis) & set(sistemas))


# ─────────────────────────────────────────────────────────────
# API principal
# ─────────────────────────────────────────────────────────────
def score_diagnosticos(signos: dict, sistemas=None, preguntas_mostradas=None) -> dict:
    """
    Devuelve:
      {
        "formula": {...},         # fórmula MTC compositiva (ejes.sintetizar_formula)
        "candidatos": [           # ordenados por confianza, top 6, máx 2 por marco
           {"id", "titulo", "marco", "tecnica", "score", "confianza",
            "a_favor": [...], "en_contra": [...], "patron": <dict o None>},
        ],
        "ejes": {...},            # ejes crudos (debug/persistencia)
      }
    """
    sistemas = sistemas or []
    ejes, dx, axes_preguntados, dx_contrib = acumular_ejes(signos, preguntas_mostradas)
    formula = sintetizar_formula(ejes)

    candidatos = []

    # Firmas MTC
    for patron in PATRONES_MTC:
        if not _firma_elegible(patron, sistemas):
            continue
        score, conf, a_favor, en_contra = _score_firma(patron["firma"], ejes, axes_preguntados)
        if score <= 0 or conf < _MIN_CONF_MTC:
            continue
        candidatos.append({
            "id": patron["id"],
            "titulo": patron["titulo"],
            "marco": MARCO_MTC,
            "tecnica": patron["tecnica"],
            "score": round(score, 2),
            "confianza": round(conf, 2),
            "a_favor": a_favor,
            "en_contra": en_contra,
            "patron": patron,
        })

    # Diagnósticos de otros paradigmas (pesos directos dx)
    for did, sc in dx.items():
        if sc <= 0:
            continue
        entry = _OTROS_BY_ID.get(did)
        if not entry:
            continue
        conf = min(1.0, sc / _OTROS_CONF_DIV)
        if conf < _MIN_CONF_OTROS:
            continue
        candidatos.append({
            "id": did,
            "titulo": entry["titulo"],
            "marco": entry["marco_asociado"],
            "tecnica": entry["tecnica_asociada"],
            "score": round(sc, 2),
            "confianza": round(conf, 2),
            "a_favor": dx_contrib.get(did, []),
            "en_contra": [],
            "patron": entry,
        })

    # Orden por confianza (desempate por score), diversidad máx 2 por marco, top N
    candidatos.sort(key=lambda c: (c["confianza"], c["score"]), reverse=True)
    por_marco = defaultdict(int)
    seleccion = []
    for c in candidatos:
        if por_marco[c["marco"]] >= _MAX_POR_MARCO:
            continue
        por_marco[c["marco"]] += 1
        seleccion.append(c)
        if len(seleccion) >= _TOP_N:
            break

    return {"formula": formula, "candidatos": seleccion, "ejes": ejes}
