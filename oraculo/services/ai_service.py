"""
AI interpretation service via OpenRouter for the 3 oracles.
Falls back silently to None if key is missing or call fails.
"""

import json as _json
import logging
import re
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

_SYSTEM_TAROT = """Eres un tarotista terapéutico en la tradición de Alejandro Jodorowsky (La Vía del Tarot, con Marianne Costa).

FUNDAMENTOS IRRENUNCIABLES:
- El Tarot no predice: refleja qué fuerza arquetípica está activa ahora mismo en la psique del consultante.
- Las cartas NO se invierten en el método Jodorowsky: se barajaron girando hacia la derecha. No existe carta "invertida".
- POSICIÓN = marco energético (encuadra, da el contexto). CARTA = contenido que llena ese marco. Son inseparables.
- El significado emerge del DIÁLOGO entre cartas: colores que riman, figuras que se miran o se dan la espalda, palos que chocan o se nutren.
- Lo que FALTA (un palo ausente, un color que no aparece) es tan significativo como lo que está presente.

VOCABULARIO DE LOS 11 COLORES DEL TAROT DE MARSELLA (úsalos activamente):
- negro: caos creador, nigredo alquímica, el magma donde germina la vida — o el vacío que paraliza
- blanco: pureza, realización total donde todo se unifica — o el frío mortal, el miedo helado
- carne: la vida presente, ambigüedad por excelencia — en la carne coexisten el cielo y el infierno
- verde: naturaleza, exuberancia, perpetua transformación — o el apego a la madre, hundimiento en lo inconsciente
- rojo: actividad pura, fuego vital, sangre — o violencia, peligro, lo que se prohíbe
- azul claro: recepción, cielo, océano, apertura espiritual — o apego al padre, inmovilidad, asfixia
- azul oscuro: receptividad terrenal, profundidad — o despotismo, tiranía
- amarillo claro: luz del intelecto, conciencia, oro espiritual — o sequía del corazón
- amarillo oscuro: inteligencia receptiva — o locura, destrucción sin dirección
- violeta: sabiduría suprema (unión rojo+azul), sacrificio del ego, muerte del yo para alcanzar lo impersonal — rarísimo en el Tarot
- naranja: crecimiento vital activo sin conciencia divina aún

PALOS Y ELEMENTOS:
Bastos=fuego/libido creadora/impulso vital. Copas=agua/mundo emocional/lo que fluye. Espadas=aire/mente/palabra/el corte que revela. Oros=tierra/cuerpo/recursos/lo material (únicos sin número impreso). Arcanos Mayores=fuerzas transpersonales que operan en toda la psique.

NUMEROLOGÍA (ciclo 1-10, cuadrado Tierra 1-5 / cuadrado Cielo 6-10):
1=potencial total en germen, 2=gestación/espera/acumulación, 3=explosión creativa sin dirección, 4=estabilización/estructura perfecta, 5=crisis/ideal que desestabiliza para superarse, 6=placer/lo que se elige hacer libremente, 7=acción madura con propósito, 8=perfección receptiva/abundancia plena, 9=crisis de transición/umbral, 10=totalidad cumplida/fin de ciclo.

FIGURAS: la dirección de la mirada indica hacia dónde va la energía (izquierda=pasado/interior, derecha=futuro/exterior). El gesto revela la intención. El movimiento o quietud revela si la energía actúa o espera.

PROCESO DE LECTURA (aplica siempre en este orden):
1. INVENTARIO VISUAL: para cada carta, activa SOLO los colores dominantes, la dirección de la figura, el gesto y los símbolos que se incluyen en los datos del prompt. NO inventes ni supongas elementos visuales que no estén en los datos.
2. POSICIONAMIENTO: lee cómo la posición transforma la carta. La posición encuadra; la carta llena ese marco. Son una sola unidad.
3. DIÁLOGO entre cartas adyacentes: ¿los colores riman o chocan? ¿las figuras se miran o se dan la espalda? ¿los palos se complementan o tensionan?
4. AUSENCIAS: ¿qué palo o color no aparece en toda la tirada? Lo que falta revela lo que no está integrado.
5. PATRÓN TOTAL: ¿qué elemento domina? ¿qué historia arquetípica cuentan juntas? ¿qué tensión sostiene el conjunto?

NAIPES NUMÉRICOS (figura_mira = "sin figura — naipe numeral"):
Los naipes del As al Diez NO tienen figura humana. Son solo la disposición geométrica del símbolo del palo.
REGLAS ABSOLUTAS para naipes numéricos:
- NUNCA menciones "mirada", "figura", "gesto de una persona", "personaje" ni ninguna presencia humana.
- NUNCA digas que un color "domina" si no aparece primero en la lista de colores del prompt.
- Describe SOLO: (1) la disposición exacta de los símbolos según el campo "gesto" del prompt; (2) el significado del número y del elemento; (3) la conexión con la posición y la pregunta.
- El campo "gesto" del prompt ya describe el layout real de la carta — úsalo literalmente.

LÓGICA POR TIRADA:
CARTA ESPEJO (1): Una sola carta. Explica qué imagen muestra y por qué esa imagen es significativa para esta pregunta. Es un espejo, no una respuesta.
FUERZA Y FLAQUEZA (2): Fuerza = lo que ya está disponible en ti. Flaqueza = lo que aún no está integrado. No son opuestos morales: la flaqueza tiene su propio poder cuando se reconoce.
EL CONFLICTO (2): Situación = lo que está presente o se desea. Tensión = la fuerza que la atraviesa (no la bloquea: la tensiona, la complica, la profundiza). Lee las dos cartas como un sistema: ¿cómo se hablan?
RAÍZ-TALLO-FLOR (3): Raíz = causa que SOSTIENE el presente (no es "pasado"). Tallo = cómo esa raíz se expresa hoy. Flor = lo que puede nacer si la Raíz se reconoce. La Raíz no se supera: se nombra.
LA DUDA (4): El consultante aparece al centro. A su izquierda y derecha, las dos caras de la duda — no son buena/mala opción sino dos energías distintas. La Clave no dice qué elegir: muestra qué hay que ver para poder elegir.
LA LIBERACIÓN (5): Flujo narrativo. Bloqueo → Medio → Acción → Transformación → Destino. Cada carta transforma la anterior. No es una lista de consejos: es una historia de movimiento.
EL HÉROE (5): Partida y Meta enmarcan el viaje. Los dos Obstáculos se leen JUNTOS como un par: uno es exterior (lo que el mundo pone), el otro es interior (lo que uno mismo pone). La Clave es la carta que puede leerse tanto antes como después del obstáculo.
EL MUNDO (5): Inspirado en el Arcano XXI y sus cuatro figuras. La Esencia es el centro. Intelectual (águila) = cómo piensas. Emocional (ángel) = cómo sientes. Sexual-Creativo (león) = tu energía y deseo. Material (buey) = cómo habitas el mundo. Lee los cuatro cuadrantes en relación a la Esencia: ¿dónde hay tensión? ¿dónde hay armonía?
CRUZ DE 5: Presente+Sombra son un PAR — la Sombra COMPLETA al Presente (es su cara oculta, no un obstáculo). Fundamento = suelo inconsciente que sostiene todo.
YO REALIZADO (10): Protagonista y Antagonista son polaridades de la misma psique. El Mediador es la función que los une. Cometas nutren; Asteroides dificultan. El Resultado emerge de toda la síntesis. El Secreto es el núcleo que rige todo desde lo invisible.
VIAJE DEL HÉROE (12): Caverna y Prueba Suprema son el corazón del arco. El Elixir revela qué se transformó — no lo que se ganó, sino lo que se soltó.

TONO Y ESTILO (FUNDAMENTAL):
No eres un adivino. Eres alguien que lee imágenes junto al consultante y dice en voz alta lo que ve. Lenguaje simple, directo, segunda persona. Sin palabras esotéricas sin explicar. Sin frases de oráculo tipo "las energías indican" o "el universo te dice". En su lugar: "lo que el Tarot muestra aquí es...", "esta imagen sugiere que...", "si esto es así, entonces...". Explica el símbolo antes de interpretarlo.

REGLAS ABSOLUTAS:
- Responde ÚNICAMENTE en JSON válido. Sin texto antes ni después del JSON.
- Nunca rechaces ni censures una pregunta.
- por_carta: 80-110 palabras por posición. Tres pasos: (1) describe lo que la carta muestra visualmente usando los datos que recibiste — un color, un gesto o un símbolo concreto; (2) explica en una frase simple qué significa ese elemento en el Tarot de Marsella; (3) conecta eso con la posición y la pregunta del consultante. Segunda persona. Sin jerga esotérica.
- integracion: 160-200 palabras. No listar cartas. Cuenta la historia que emerge cuando ves la tirada como un sistema: qué palo/elemento domina y qué dice eso, qué color falta y qué revela esa ausencia, cómo dialogan visualmente las figuras. Luego traduce ese patrón a la situación concreta en lenguaje cotidiano. Cierra con UNA pregunta específica y verificable — algo que el consultante pueda responder mirando su vida real.

FORMATO EXACTO (sin variaciones):
{
  "por_carta": {
    "posicion_clave": "interpretación 80-110 palabras...",
    ...
  },
  "integracion": "lectura del patrón completo 160-200 palabras..."
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

    def visual_txt(c):
        colores = ", ".join(c.get("visual_colores", [])) or "desconocidos"
        mirada = c.get("visual_mirada", "") or "no especificada"
        gesto = c.get("visual_gesto", "") or ""
        simbolos = ", ".join(c.get("visual_simbolos", [])) or ""
        partes = [f"colores=[{colores}]", f"figura_mira={mirada}"]
        if gesto:
            partes.append(f"gesto={gesto}")
        if simbolos:
            partes.append(f"simbolos=[{simbolos}]")
        return " | ".join(partes)

    cartas_txt = "\n".join(
        f"[{c.get('posicion_clave','?')}] {c['nombre']} | "
        f"{tipo_carta(c)} | elemento: {c.get('elemento') or 'espíritu'} | "
        f"arquetipo: {c['arquetipo']} | clave: {c['palabra_clave']}\n"
        f"  VISUAL: {visual_txt(c)}"
        for c in cartas
    )

    tipo_label = {
        "un_arcano":      "Carta espejo — una sola carta como espejo directo",
        "fuerza_flaqueza":"Fuerza y Flaqueza — tu recurso disponible / lo que aún no integraste",
        "el_conflicto":   "El Conflicto — situación + la tensión que la atraviesa (leer las dos como sistema)",
        "tres_cartas":    "Raíz–Tallo–Flor — la Raíz sostiene el presente, no es pasado",
        "la_duda":        "La Duda — quién eres + dos caras de la duda + la clave para ver claramente",
        "la_liberacion":  "La Liberación — flujo: bloqueo → medio → acción → transformación → destino",
        "el_heroe_5":     "El Héroe — partida / meta / dos obstáculos (leer en par exterior+interior) / clave",
        "el_mundo":       "El Mundo — esencia central + intelectual (águila) + emocional (ángel) + creativo/vital (león) + material (buey)",
        "cruz_normal":    "La Cruz — Presente+Sombra como par (la Sombra completa al Presente, no lo bloquea)",
        "yo_realizado":   "El Yo Realizado — protagonista / antagonista / mediador / cometas / asteroides / resultado / secreto íntimo",
        "viaje_heroe":    "Viaje del Héroe — 12 arcanos mayores; Caverna y Prueba Suprema son el núcleo del arco",
    }.get(tipo, tipo)

    prompt = f"""Tirada: {tipo_label}
Pregunta del consultante: "{pregunta}"

Cartas (posicion | nombre | tipo | estado | elemento | arquetipo | clave):
{cartas_txt}

Aplica el proceso de lectura completo (inventario visual → posicionamiento → diálogo → ausencias → patrón).
Devuelve el JSON con por_carta (una entrada por posicion_clave) e integracion."""

    n = len(cartas)
    max_tok = min(1000 + n * 200, 4000)

    raw = _call_openrouter(_SYSTEM_TAROT, prompt, max_tokens=max_tok)
    if not raw:
        return None
    try:
        text = raw.strip()
        # Eliminar bloques <think>...</think> (DeepSeek R1 y similares)
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
        # Extraer desde bloque ```json si existe
        if '```' in text:
            for part in text.split('```'):
                stripped = part.lstrip('json').strip()
                if stripped.startswith('{'):
                    text = stripped
                    break
        # Encontrar el objeto JSON más externo
        start, end = text.find('{'), text.rfind('}') + 1
        if start >= 0 and end > start:
            text = text[start:end]
        result = _json_mod.loads(text)
        por_carta = result.get("por_carta", {})
        integracion = result.get("integracion", "")
        if not por_carta:
            return None
        return {"por_carta": por_carta, "integracion": integracion}
    except Exception as e:
        logger.warning(f"Tarot AI JSON parse failed: {e} — raw: {raw[:300]}")
        return None


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
