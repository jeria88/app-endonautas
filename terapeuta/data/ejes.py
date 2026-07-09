"""
Ejes diagnósticos de Medicina Tradicional China (Ba Gang + factores + órganos).

El diagnóstico MTC no es elegir un ítem de una lista: es componer una fórmula
desde ejes (Manual MTC, Parte 5.5):

    Patrón = [Exterior/Interior] + [Deficiencia/Exceso] + [Frío/Calor]
             + [Órgano/Sustancia] + [Factor patógeno] + [Fase]

Cada opción de respuesta en `anamnesis.py` puntúa ejes, no diagnósticos.
El motor (`scoring.py`) acumula ejes desde las respuestas, sintetiza la fórmula
y hace match contra las firmas de `patrones_mtc.py`.

Tipos de eje:
  - BIPOLAR: valor con signo. Positivo = primer polo, negativo = segundo.
  - UNIPOLAR: se acumula (≥0 normalmente); un peso negativo es discriminante
    en contra (ej. "sin sed" resta al eje de Calor).
"""

# ─────────────────────────────────────────────────────────────
# Ejes BIPOLARES (Ba Gang — los cuatro pares de Kaptchuk cap. 7)
# ─────────────────────────────────────────────────────────────
# clave: (polo_positivo, polo_negativo)
EJES_BIPOLARES = {
    "termico":     ("Calor", "Frío"),        # han/re
    "plenitud":    ("Exceso", "Deficiencia"),  # shi/xu
    "profundidad": ("Exterior", "Interior"),   # biao/li
}

# Eje térmico observado SOLO en lengua/observación (Wang-zhen).
# Sirve para detectar Calor Verdadero/Frío Ilusorio (Manual 5.4): si el térmico
# de los síntomas contradice el de la lengua, la lengua arbitra.
EJE_LENGUA = "termico_lengua"

# ─────────────────────────────────────────────────────────────
# Ejes UNIPOLARES — factores patógenos (Liu Yin) y productos (Tan, Xue Yu)
# ─────────────────────────────────────────────────────────────
EJES_FACTORES = {
    "viento":       "Viento (Feng)",
    "humedad":      "Humedad (Shi)",
    "sequedad":     "Sequedad (Zao)",
    "tan":          "Mucosidad / Flema (Tan)",
    "estasis":      "Estasis de Sangre (Xue Yu)",
    "calor_sangre": "Calor en Sangre (Xue Re)",
    "qi_zhi":       "Estancamiento de Qi (Qi Zhi)",
}

# ─────────────────────────────────────────────────────────────
# Ejes UNIPOLARES — sustancias deficientes
# ─────────────────────────────────────────────────────────────
EJES_SUSTANCIAS = {
    "qi_def":   "Deficiencia de Qi",
    "xue_def":  "Deficiencia de Sangre (Xue Xu)",
    "yin_def":  "Deficiencia de Yin",
    "yang_def": "Deficiencia de Yang",
}

# ─────────────────────────────────────────────────────────────
# Ejes UNIPOLARES — órganos (Zang-Fu). Acumulan evidencia de localización,
# emoción→órgano (Manual 1.4B), cualidad del dolor y mapa de lengua (3.2D).
# ─────────────────────────────────────────────────────────────
EJES_ORGANOS = {
    "higado":   "Hígado",
    "corazon":  "Corazón",
    "bazo":     "Bazo",
    "pulmon":   "Pulmón",
    "rinon":    "Riñón",
    "estomago": "Estómago",
    "ig":       "Intestino Grueso",
}

# Conjunto plano de todos los ejes válidos (para validación).
TODOS_LOS_EJES = (
    set(EJES_BIPOLARES)
    | {EJE_LENGUA}
    | set(EJES_FACTORES)
    | set(EJES_SUSTANCIAS)
    | set(EJES_ORGANOS)
)

# Umbral por debajo del cual un eje se considera ruido y no entra en la fórmula.
UMBRAL_FACTOR = 1.5
UMBRAL_ORGANO = 1.5


def eje_label(axis, positivo=True):
    """Frase legible para un eje en una dirección dada (para a_favor/en_contra)."""
    if axis in EJES_BIPOLARES:
        polo_pos, polo_neg = EJES_BIPOLARES[axis]
        return polo_pos if positivo else polo_neg
    if axis == EJE_LENGUA:
        return "Lengua: signos de Calor" if positivo else "Lengua: signos de Frío"
    if axis in EJES_FACTORES:
        base = EJES_FACTORES[axis]
        return base if positivo else f"Ausencia de {base}"
    if axis in EJES_SUSTANCIAS:
        base = EJES_SUSTANCIAS[axis]
        return base if positivo else f"Sin signos de {base}"
    if axis in EJES_ORGANOS:
        return f"Compromiso de {EJES_ORGANOS[axis]}"
    return axis


def sintetizar_formula(ejes: dict) -> dict:
    """
    Compone la fórmula Ba Gang desde los ejes acumulados (Manual 5.5).

    Devuelve un dict con los componentes y un `texto` legible, más un flag
    `contradiccion` (Manual 5.4) cuando el térmico sintomático contradice la
    lengua — en ese caso la lengua arbitra.
    """
    termico_sintomas = ejes.get("termico", 0)
    termico_lengua = ejes.get(EJE_LENGUA, 0)

    # Detección de Calor Verdadero / Frío Ilusorio (5.4): la lengua arbitra.
    contradiccion = None
    termico_final = termico_sintomas
    if termico_lengua != 0 and termico_sintomas != 0 and \
            (termico_lengua > 0) != (termico_sintomas > 0):
        contradiccion = (
            "Los síntomas y la lengua apuntan a temperaturas opuestas "
            "(posible Calor Verdadero/Frío Ilusorio, Manual 5.4). "
            "La lengua arbitra: se prioriza su signo."
        )
        termico_final = termico_lengua
    elif termico_lengua != 0:
        # sin contradicción: la lengua refuerza el térmico global
        termico_final = termico_sintomas + termico_lengua

    def polo(axis, valor, umbral=0.5):
        if abs(valor) < umbral:
            return None
        pos, neg = EJES_BIPOLARES[axis]
        return pos if valor > 0 else neg

    profundidad = polo("profundidad", ejes.get("profundidad", 0))
    plenitud = polo("plenitud", ejes.get("plenitud", 0))
    termico = None
    if abs(termico_final) >= 0.5:
        termico = "Calor" if termico_final > 0 else "Frío"

    # órganos ordenados por evidencia
    organos = sorted(
        ((EJES_ORGANOS[k], ejes.get(k, 0)) for k in EJES_ORGANOS if ejes.get(k, 0) >= UMBRAL_ORGANO),
        key=lambda t: -t[1],
    )
    organos_nombres = [n for n, _ in organos[:3]]

    # factores patógenos presentes
    factores = [
        EJES_FACTORES[k] for k in EJES_FACTORES
        if ejes.get(k, 0) >= UMBRAL_FACTOR
    ]

    # sustancias deficientes
    sustancias = [
        EJES_SUSTANCIAS[k] for k in EJES_SUSTANCIAS
        if ejes.get(k, 0) >= UMBRAL_FACTOR
    ]

    # texto compositivo estilo "Interior · Exceso-Calor · Viento en Pulmón"
    partes = []
    if profundidad:
        partes.append(profundidad)
    plen_term = "-".join(x for x in (plenitud, termico) if x)
    if plen_term:
        partes.append(plen_term)
    if factores:
        partes.append(" + ".join(factores))
    if sustancias:
        partes.append(" + ".join(sustancias))
    if organos_nombres:
        partes.append("en " + " / ".join(organos_nombres))
    texto = " · ".join(partes) if partes else "Patrón no diferenciado (falta información)"

    return {
        "profundidad": profundidad,
        "plenitud": plenitud,
        "termico": termico,
        "organos": organos_nombres,
        "factores": factores,
        "sustancias": sustancias,
        "texto": texto,
        "contradiccion": contradiccion,
    }
