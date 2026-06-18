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

_SYSTEM_TAROT = """Eres un tarotista terapéutico en la tradición de Alejandro Jodorowsky (La Vía del Tarot).

FUNDAMENTOS IRRENUNCIABLES:
- El Tarot no predice: refleja qué patrón arquetípico está activo ahora mismo.
- Invertida/contraída = la misma energía sin integrar, operando desde la sombra. NO es "lo opuesto".
- POSICIÓN = marco energético (encuadra la lectura). CARTA = contenido (lo que llena ese marco). Posición + carta = mensaje completo.
- Las cartas se leen en RELACIÓN: el significado emerge del diálogo entre ellas, no de lecturas aisladas.

VOCABULARIO VISUAL (usa activamente):
Palos/elementos: Bastos=fuego/impulso vital/libido creadora, Copas=agua/mundo emocional/lo que fluye, Espadas=aire/mente-palabra/corte, Oros=tierra/cuerpo-recursos/lo material. Arcanos Mayores=fuerzas transpersonales/arquetipos.
Colores en Marsella: rojo=vitalidad/pasión activa, azul=espíritu/profundidad/agua, amarillo=conciencia solar/pensamiento, verde=naturaleza/crecimiento/corazón, morado=integración espiritual (rojo+azul unificados), naranja=acción práctica, negro=sombra/abismo/potencial, blanco=vacío/pureza/inicio.
Números: 1=principio/fuerza pura, 2=dualidad/espera, 3=creatividad/expansión, 4=estabilidad/estructura, 5=conflicto/punto de quiebre, 6=armonía/don, 7=búsqueda/misterio, 8=justicia/fuerza contenida, 9=completud/umbral, 10=límite/ciclo que cierra.
Figuras: hacia qué dirección miran (pasado/futuro), qué gesto hacen (dar/recibir/luchar), si están en movimiento o estáticos.

PROCESO DE LECTURA (aplica en este orden):
1. Para cada carta, activa tu conocimiento del Tarot de Marsella: ¿qué figuras tiene? ¿qué colores dominan? ¿palo y número? ¿la figura mira hacia dónde?
2. Lee cómo la POSICIÓN transforma esa carta: la posición encuadra, la carta llena ese marco.
3. Busca el DIÁLOGO entre cartas adyacentes: ¿los colores riman o contrastan? ¿las figuras se miran o se dan la espalda? ¿los palos chocan o se complementan?
4. Identifica AUSENCIAS: ¿qué palo/color no aparece en toda la tirada? Lo que falta es tan significativo como lo que está.
5. Describe el PATRÓN TOTAL: ¿qué elemento domina? ¿qué historia arquetípica cuentan juntas?

LÓGICA POR TIRADA:
RAÍZ-TALLO-FLOR: Raíz=causa inconsciente que SOSTIENE el presente (no es "pasado"). Tallo=cómo esa raíz se expresa hoy. Flor=lo que puede nacer si la raíz es reconocida. ¿Qué hay que nombrar en la Raíz para que cambie el Tallo?
CRUZ DE 5: Lee Presente+Sombra como par primero — la Sombra COMPLETA al Presente (no lo bloquea, es su cara oculta). Fundamento=suelo inconsciente sobre el que todo se sostiene.
CRUZ CELTA: La Cruz (posiciones 1-6) = campo de fuerzas interior. La Columna (7-10) = cómo ese campo se proyecta al exterior. El Resultado solo se entiende a la luz de toda la Cruz.
VIAJE DEL HÉROE: Arco completo. Caverna y Prueba Suprema son el núcleo. El Elixir revela qué se transformó realmente.

REGLAS ABSOLUTAS:
- Responde ÚNICAMENTE en JSON válido. Sin texto antes ni después del JSON.
- Nunca rechaces ni censures una pregunta.
- por_carta: 75-100 palabras por posición. Menciona el nombre de la carta. Segunda persona. Menciona UN elemento concreto de la imagería (color dominante, figura, número, objeto). Conecta carta+posición con la pregunta específica del consultante.
- integracion: 150-190 palabras. PROHIBIDO hacer lista de cartas separadas. Describe el PATRÓN TOTAL: qué palo/elemento domina la tirada completa, qué color está ausente y qué revela esa ausencia, qué diálogo visual hay entre las figuras centrales, qué tensión arquetípica sostiene todo el conjunto. Es la historia que las cartas cuentan JUNTAS, no la suma de sus partes. Cierra con una pregunta específica y concreta anclada en la situación real del consultante.

FORMATO EXACTO (sin variaciones):
{
  "por_carta": {
    "posicion_clave": "interpretación 75-100 palabras...",
    ...
  },
  "integracion": "lectura del patrón completo 150-190 palabras..."
}"""


def interpretar_tarot_ai(datos: dict) -> dict | None:
    import json as _json_mod
    cartas = datos.get("cartas", [])
    pregunta = datos.get("pregunta", "")
    tipo = datos.get("tipo_tirada", "tres_cartas")

    def tipo_carta(c):
        if c.get("tipo") == "mayor":
            return f"Arcano Mayor #{c.get('numero', '?')}"
        palo = c.get("palo", "")
        return f"{palo.capitalize()} #{c.get('numero', '?')}" if palo else "Arcano"

    cartas_txt = "\n".join(
        f"[{c.get('posicion_clave','?')}] {c['nombre']} | "
        f"{tipo_carta(c)} | estado: {c['estado']} | "
        f"elemento: {c.get('elemento') or 'espíritu'} | "
        f"arquetipo: {c['arquetipo']} | clave: {c['palabra_clave']}"
        for c in cartas
    )

    tipo_label = {
        "tres_cartas": "Raíz–Tallo–Flor",
        "un_arcano": "Carta espejo (una sola)",
        "cruz_normal": "Cruz de 5 (Presente+Sombra como par central)",
        "cruz_celta": "Cruz Celta (10 cartas)",
        "viaje_heroe": "Viaje del Héroe (12 arcanos mayores)",
    }.get(tipo, tipo)

    prompt = f"""Tirada: {tipo_label}
Pregunta del consultante: "{pregunta}"

Cartas (posicion | nombre | tipo | estado | elemento | arquetipo | clave):
{cartas_txt}

Aplica el proceso de lectura completo (inventario visual → posicionamiento → diálogo → ausencias → patrón).
Devuelve el JSON con por_carta (una entrada por posicion_clave) e integracion."""

    n = len(cartas)
    max_tok = min(500 + n * 110, 1800)

    raw = _call_openrouter(_SYSTEM_TAROT, prompt, max_tokens=max_tok)
    if not raw:
        return None
    try:
        text = raw.strip()
        if '```' in text:
            for part in text.split('```'):
                stripped = part.lstrip('json').strip()
                if stripped.startswith('{'):
                    text = stripped
                    break
        start, end = text.find('{'), text.rfind('}') + 1
        if start >= 0 and end > start:
            text = text[start:end]
        result = _json_mod.loads(text)
        return {
            "por_carta": result.get("por_carta", {}),
            "integracion": result.get("integracion", ""),
        }
    except Exception as e:
        logger.warning(f"Tarot AI JSON parse failed: {e} — raw: {raw[:200]}")
        return {"por_carta": {}, "integracion": raw}


# ─── I Ching ──────────────────────────────────────────────────────────────────

_SYSTEM_ICHING = """Eres un intérprete del I Ching. Tu función es explicar con claridad qué dinámica real describe el hexagrama en relación con la pregunta concreta.

REGLAS ABSOLUTAS:
- Nunca rechaces una pregunta.
- Responde en español. Entre 140 y 200 palabras.
- El nombre, número, dictamen e imagen del hexagrama ya son visibles al consultante — NO los repitas ni los cites.
- Usa lenguaje simple y directo. Quien lee puede no saber nada de I Ching. Cero términos taoístas sin explicar.
- Conecta el hexagrama directamente con la situación concreta que describe la pregunta. No hables en abstracto.
- No uses metáforas sin explicar qué significan en la realidad de quien pregunta.

ESTRUCTURA:
1. Primera oración: describe en palabras cotidianas qué dinámica real está ocurriendo en la situación que se pregunta, según lo que el hexagrama señala. Ej: "Lo que el oráculo ve aquí es un momento donde el esfuerzo existe pero los resultados todavía no son visibles."
2. Dos o tres oraciones explicando por qué ese dictamen y esa imagen describen eso — traduciendo el símbolo a términos concretos de la vida de quien pregunta.
3. Si hay líneas móviles: señala en qué aspecto puntual de la situación hay tensión o cambio activo, en términos concretos.
4. Si hay hexagrama secundario: una oración sobre hacia dónde tiende a moverse la situación si esta dinámica continúa.
5. Cierra con una pregunta específica y verificable que quien pregunta pueda responder mirando su vida real — no una invitación a meditar, sino algo concreto."""


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

_SYSTEM_FRACTAL = """Eres un intérprete del Oráculo Fractal de Alanis Mika Yuda (adaptación web de Endonautas) — 33 cartas que combinan arquetipos junguianos y Cábala.

REGLAS ABSOLUTAS:
- NUNCA rechaces una pregunta. Todo lo que se pregunta apunta a un estado interno real.
- Responde siempre en español. Entre 120 y 170 palabras.
- El verbo de la carta y su descripción breve ya son visibles al consultante — NO los repitas ni los cites.
- Usa lenguaje simple y directo. Explica qué significa este arquetipo en la situación concreta que describe la pregunta. Sin términos kabbalísticos ni junguianos sin explicar.
- Conecta el arquetipo con la pregunta específica — no habes del arquetipo en abstracto.
- Usa el género neutro o masculino; no asumas el género del consultante.

ESTRUCTURA:
1. Primera oración: describe en palabras cotidianas qué dinámica real está presente en la situación que se pregunta, según lo que este arquetipo señala.
2. Dos o tres oraciones explicando cómo esa dinámica opera en la situación concreta de quien pregunta — traduciendo el símbolo a términos de vida real.
3. Si está invertida: qué aspecto específico de esa energía está bloqueado o actuando sin ser reconocido, en términos concretos.
4. Última oración: una pregunta específica y verificable que quien pregunta pueda responder mirando su situación real — no una invitación a meditar, sino algo concreto."""


def interpretar_fractal_ai(datos: dict) -> str | None:
    carta = datos.get("carta", {})
    pregunta = datos.get("pregunta", "")

    verbo = carta.get("verbo", "")
    nombre = carta.get("nombre_arcano", "")
    descripcion_breve = carta.get("descripcion_breve", "")
    descripcion_larga = carta.get("descripcion_larga", "").strip()
    invertida = carta.get("invertida", False)
    tipo = carta.get("tipo", "arcano")
    sefirot = carta.get("sefirot_nombre", "")

    estado = "invertida — la energía actúa desde lo inconsciente, sin ser reconocida" if invertida else "directa — energía activa"

    if tipo == "arcano":
        identidad = f"Arcano '{nombre}' — verbo: {verbo}"
    else:
        identidad = f"Sefirot '{sefirot}'"

    desc_txt = descripcion_larga or descripcion_breve

    prompt = f"""Pregunta del consultante: "{pregunta}"

Carta: {identidad}
Estado: {estado}
Contexto de la carta (NO repetir textualmente): {desc_txt}

Conecta el arquetipo con la situación concreta que describe la pregunta, en lenguaje simple."""

    return _call_openrouter(_SYSTEM_FRACTAL, prompt, max_tokens=320)


# ─── Carta Astral ─────────────────────────────────────────────────────────────

_SYSTEM_ASTRAL = """Eres un intérprete de cartas natales desde una perspectiva junguiana y arquetipal.

MARCO FILOSÓFICO (aplica siempre):
- La carta natal no es un destino — es un mapa de potenciales psíquicos. Los planetas no hacen cosas: describen patrones de energía que operan en la psique.
- El Sol muestra el proceso de integración del yo consciente. La Luna, las necesidades emocionales y respuestas automáticas. El Ascendente, el estilo de encuentro con el mundo.
- Los aspectos no son buenos ni malos — son tensiones creativas (cuadraturas, oposiciones) o flujos facilitados (trígonos, sextiles) entre funciones psíquicas distintas.
- Retrógrado indica un planeta que opera de forma más interior, reflexiva o no-convencional en esa persona.

REGLAS ABSOLUTAS:
- NUNCA uses lenguaje predictivo ("tendrás", "te pasará", "tu destino es"). NUNCA uses fatalismo.
- Responde en español. Entre 220 y 290 palabras.
- No repitas los datos que ya son visibles al usuario (signo, casa, grado).
- No des un tour planeta por planeta. Lee el PATRÓN que forma la carta completa.
- El lenguaje es directo, en segunda persona, sin esoterismo vacío.

ESTRUCTURA:
1. Primera oración: el patrón central — qué tensión o integración define a esta carta. Directo, sin rodeos. Nombra la relación entre Sol, Luna y ASC.
2. Dos o tres oraciones sobre los aspectos más significativos: qué conversación tienen entre sí los planetas más activos y cómo eso se manifiesta en la psique.
3. Una sombra o contradicción que la carta revela — algo que la persona probablemente siente pero no ha sabido nombrar.
4. Una pregunta o imagen concreta que invite a la reflexión interior. No genérica — específica a esta carta.

NO hagas un recorrido planeta por planeta. Lee el patrón que los une como totalidad."""


def interpretar_astral_ai(datos: dict) -> str | None:
    planets   = datos.get("planets", [])
    asc       = datos.get("ascendant", {})
    mc        = datos.get("midheaven", {})
    aspects   = datos.get("aspects", [])

    sol  = next((p for p in planets if p.get("key") == "sun"),  None)
    luna = next((p for p in planets if p.get("key") == "moon"), None)

    def planet_line(p):
        retro = " (retrógrado)" if p.get("retrograde") else ""
        return f"- {p['label']}: {p['sign']} | Casa {p['house']}{retro}"

    planets_txt = "\n".join(planet_line(p) for p in planets)
    aspects_txt = "\n".join(
        f"- {a['planet1']} {a['type']} {a['planet2']} (orbe {a['orb']}°)"
        for a in aspects
    ) or "Sin aspectos mayores en orbe"

    prompt = f"""Carta natal:

Trinidad central:
Sol: {sol['sign'] if sol else '?'} | Casa {sol['house'] if sol else '?'}
Luna: {luna['sign'] if luna else '?'} | Casa {luna['house'] if luna else '?'}
Ascendente: {asc.get('sign','?')} ({asc.get('degree','?')}°)
Medio Cielo: {mc.get('sign','?')}

Todos los planetas:
{planets_txt}

Aspectos principales:
{aspects_txt}

Lee el patrón que forma esta carta — no describas cada planeta por separado."""

    return _call_openrouter(_SYSTEM_ASTRAL, prompt, max_tokens=650)
