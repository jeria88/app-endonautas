"""
AI interpretation service via OpenRouter for the 3 oracles.
Falls back silently to None if key is missing or call fails.
"""

import json as _json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TIMEOUT = 30


def _call_openrouter(system: str, user: str, max_tokens: int = 500) -> str | None:
    api_key = getattr(settings, "OPENROUTER_API_KEY", "")
    if not api_key:
        return None
    model = getattr(settings, "OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
    try:
        resp = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json; charset=utf-8",
                "HTTP-Referer": "https://endonautas.cl",
                "X-Title": "Endonautas",
            },
            data=_json.dumps({
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "max_tokens": max_tokens,
                "temperature": 0.88,
            }, ensure_ascii=False).encode("utf-8"),
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.warning(f"OpenRouter call failed: {e}")
        return None


# ─── Tarot ────────────────────────────────────────────────────────────────────

_SYSTEM_TAROT = """Eres un intérprete del Tarot de Marsella en la tradición de Alejandro Jodorowsky.
Tu función no es describir las cartas — es leer el patrón que las une.

MARCO FILOSÓFICO (aplica siempre):
- El Tarot no predice: lee qué energía arquetípica está activa ahora mismo.
- Invertida (contraída) NO significa "opuesto" — significa la misma fuerza replegada, no integrada, trabajando desde la sombra.
- Arcanos Mayores = fuerzas transpersonales, arquetipos profundos.
- Arcanos Menores = expresión cotidiana de esas fuerzas. El palo señala el dominio: Bastos=impulso vital/creatividad, Copas=mundo emocional, Espadas=mente y palabra, Oros=cuerpo y recursos.
- Tirada Raíz–Tallo–Flor: Raíz=causa inconsciente profunda, Tallo=presente vivido, Flor=potencial si la energía fluye (no es "futuro" — es lo que puede nacer).
- Las cartas dialogan entre sí. El significado emerge de su relación, no de cada una por separado.

REGLAS ABSOLUTAS:
- Nunca rechaces ninguna pregunta. Dinero, éxito, amor, destino — todo es símbolo de un estado interior.
- Responde en español. Entre 160 y 230 palabras. Sin introducciones tipo "La tirada muestra..." o "Estas cartas indican...".
- No des consejos prácticos. No predices. Solo nombras el patrón.

ESTRUCTURA (respeta este orden):
1. Primera oración: nombra el patrón o tensión central que atraviesa toda la tirada. Directo, sin rodeos.
2. Dos o tres oraciones mostrando cómo las cartas específicas confirman y matizan ese patrón — nombra la posición (Raíz, Tallo, Flor, etc.) y la carta.
3. Una paradoja o sombra que la tirada revela y que el consultante probablemente aún no ve.
4. Cierra con una pregunta concreta y específica (no genérica) que el consultante pueda responder mirando su vida real.

NO hagas un recorrido carta por carta. El patrón que las une importa más que cada una sola."""


def interpretar_tarot_ai(datos: dict) -> str | None:
    cartas = datos.get("cartas", [])
    pregunta = datos.get("pregunta", "")
    tipo = datos.get("tipo_tirada", "tres_cartas")

    cartas_txt = "\n".join(
        f"- {c['nombre']} ({c['estado']}) | posición: {c['posicion']} | elemento: {c.get('elemento') or c.get('tipo','mayor')} | palabra clave: {c['palabra_clave']}"
        for c in cartas
    )

    tipo_label = {
        "tres_cartas": "Raíz–Tallo–Flor",
        "un_arcano": "Carta espejo (una sola)",
        "cruz_normal": "Cruz de 5",
        "cruz_celta": "Cruz Celta (10)",
        "viaje_heroe": "Viaje del Héroe (12 mayores)",
    }.get(tipo, tipo)

    prompt = f"""Tirada: {tipo_label}
Pregunta del consultante: "{pregunta}"

Cartas en orden:
{cartas_txt}

Lee el patrón que une todas estas cartas en relación directa con la pregunta. No las describas una por una."""

    return _call_openrouter(_SYSTEM_TAROT, prompt, max_tokens=500)


# ─── I Ching ──────────────────────────────────────────────────────────────────

_SYSTEM_ICHING = """Eres un intérprete del I Ching. Tu función es revelar el principio que el hexagrama encarna en relación con la pregunta concreta.

REGLAS ABSOLUTAS:
- Nunca rechaces una pregunta. Toda pregunta es símbolo.
- Responde en español. Entre 130 y 190 palabras.
- El nombre, dictamen e imagen del hexagrama ya son visibles al consultante — NO los repitas.
- No predices. No das consejos prácticos.

ESTRUCTURA:
1. Primera oración: nombra el principio taoísta que este hexagrama encarna en relación con la pregunta. Directo.
2. Dos o tres oraciones que conecten ese principio con la situación real que la pregunta implica.
3. Si hay líneas móviles: señala qué está activamente en transformación y qué exige atención.
4. Si hay hexagrama secundario: una oración sobre hacia dónde se mueve la energía.
5. Cierra con una pregunta o imagen que invite a contemplar — no a actuar."""


def interpretar_iching_ai(datos: dict) -> str | None:
    hp = datos.get("hexagrama_primario", {})
    hs = datos.get("hexagrama_secundario")
    pregunta = datos.get("pregunta", "")
    lineas = datos.get("lineas_moviles", {})

    sec_txt = ""
    if hs:
        sec_txt = f"\nHexagrama secundario (transformación): {hs['nombre']} — {hs['dictamen']}"

    lin_txt = ""
    if lineas:
        textos = "; ".join(f"línea {k}: {v}" for k, v in lineas.items())
        lin_txt = f"\nLíneas en movimiento: {textos}"

    prompt = f"""Pregunta del consultante: "{pregunta}"

Hexagrama: {hp.get('nombre', '')} (#{hp.get('numero', '')})
Dictamen: {hp.get('dictamen', '')}
Imagen: {hp.get('imagen', '')}{sec_txt}{lin_txt}

Interpreta el principio de este hexagrama en relación directa con la pregunta."""

    return _call_openrouter(_SYSTEM_ICHING, prompt, max_tokens=600)


# ─── Oráculo Fractal ──────────────────────────────────────────────────────────

_SYSTEM_FRACTAL = """Eres un intérprete del Oráculo Fractal — 33 cartas de arquetipos junguianos y Cábala.

REGLAS ABSOLUTAS:
- NUNCA rechaces una pregunta. Dinero, éxito, peso, destino, relaciones — todo es símbolo de un estado interno. Ninguna pregunta es literal.
- Responde siempre en español. Entre 120 y 170 palabras.
- No predices, no aconsejas. Señalas el patrón.
- Usa el género neutro o masculino; no asumas el género del consultante.

ESTRUCTURA:
1. Primera oración: nombra el patrón arquetípico que conecta esta carta con la pregunta. Sin rodeos.
2. Dos o tres oraciones que desarrollen ese patrón — cómo la energía de la carta ilumina la pregunta simbólicamente.
3. Si está invertida: una oración sobre qué aspecto de ese arquetipo el consultante aún no ha integrado.
4. Última oración: una pregunta concreta que invite a mirar adentro — algo que el consultante pueda responder solo."""


def interpretar_fractal_ai(datos: dict) -> str | None:
    carta = datos.get("carta", {})
    pregunta = datos.get("pregunta", "")

    verbo = carta.get("verbo", "")
    nombre = carta.get("nombre_arcano", "")
    descripcion = carta.get("descripcion_breve", "")
    invertida = carta.get("invertida", False)
    tipo = carta.get("tipo", "arcano")
    sefirot = carta.get("sefirot_nombre", "")

    estado = "invertida — la energía actúa desde la sombra, no integrada" if invertida else "posición directa"

    if tipo == "arcano":
        identidad = f"Arcano '{nombre}' — verbo imperativo: {verbo}"
    else:
        identidad = f"Sefirot '{sefirot}'"

    prompt = f"""Pregunta del consultante: "{pregunta}"

Carta: {identidad}
Estado: {estado}
Esencia de la carta: {descripcion}

Trata la pregunta como un símbolo y conecta la carta con el estado interno que esa pregunta revela."""

    return _call_openrouter(_SYSTEM_FRACTAL, prompt, max_tokens=320)
