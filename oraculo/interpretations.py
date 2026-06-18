"""
Módulo de interpretaciones para los 3 oráculos.

Intenta primero una interpretación vía OpenRouter (AI).
Si la clave no está configurada o la llamada falla, usa plantillas estáticas potentes.
"""

import random

from .services.ai_service import (
    interpretar_tarot_ai,
    interpretar_iching_ai,
    interpretar_fractal_ai,
)


# ═══════════════════════════════════════════════════
# INTERPRETACIONES DE TAROT (Junguiano/Narrativo)
# ═══════════════════════════════════════════════════

# Frases base para cada posición de la tirada
FRASES_POSICION_TAROT = {
    # ── Tirada Raíz–Tallo–Flor (Jodorowsky) ─────────────────────────────────
    "raiz": {
        "directa": [
            "En la raíz inconsciente de lo que consultas vive {arquetipo}. Es la tierra en que todo lo demás crece — aunque no la hayas visto.",
            "La causa profunda de esta situación porta la energía de {arquetipo}. Tu psique lleva tiempo procesando este patrón sin nombrarlo.",
            "Bajo la pregunta que hiciste, {arquetipo} opera como fuerza formativa. Esta es la semilla de todo lo que estás viviendo.",
        ],
        "contraída": [
            "En la raíz, {arquetipo} trabaja desde la sombra — no integrada, replegada sobre sí misma. Algo en ese origen no ha sido aceptado del todo.",
            "La energía de {arquetipo} en la raíz está contraída: actúa, pero de manera indirecta, difícil de reconocer. Lo que no se nombra, gobierna.",
            "En el fondo de esta situación, {arquetipo} pulsa sin poder expresarse. La negación de esa fuerza es parte del patrón.",
        ],
    },
    "tallo": {
        "directa": [
            "El presente vivido lleva la marca de {arquetipo}. Esto es lo que ocurre ahora, independiente de lo que crees que ocurre.",
            "En el tallo — lo que sostienes hoy — {arquetipo} es la energía en acción. Tu psique te muestra esto como espejo.",
            "El momento actual está atravesado por {arquetipo}. No es solo una situación: es una fuerza arquetípica que pide ser reconocida.",
        ],
        "contraída": [
            "En el presente, {arquetipo} aparece contraída: la energía existe, pero no fluye. Hay resistencia a reconocer esta fuerza en tu vida actual.",
            "El tallo muestra {arquetipo} replegada sobre sí misma. Algo en lo que vives hoy actúa desde la sombra de esa energía.",
            "La fuerza de {arquetipo} opera en tu presente sin ser reclamada. La carta no describe lo que falta — describe lo que no se ve.",
        ],
    },
    "flor": {
        "directa": [
            "Lo que puede florecer, si la energía fluye, es {arquetipo}. No es predicción — es el potencial real que la situación porta.",
            "La flor de este momento apunta a {arquetipo}. Si la raíz es reconocida y el tallo no se tuerce, esto es lo que emerge.",
            "El potencial de este instante se conecta con {arquetipo}. La pregunta no es si ocurrirá — es si estás dispuesto a recibirlo.",
        ],
        "contraída": [
            "El potencial muestra {arquetipo} contraída: hay un florecimiento posible que algo en ti aún no deja llegar.",
            "La flor aparece replegada: la energía de {arquetipo} está presente pero no encuentra salida. ¿Qué la contiene?",
            "Lo que podría nacer carga la sombra de {arquetipo}. El potencial existe, pero hay una resistencia interior que merece atención.",
        ],
    },
    # ── Retrocompatibilidad (tiradas antiguas) ────────────────────────────────
    "origen": {
        "derecha": [
            "El origen de esta situación porta la energía de {arquetipo}. Tu inconsciente ha estado procesando este patrón.",
        ],
        "invertida": [
            "En el origen, {arquetipo} trabaja desde la sombra — sin ser del todo reconocida ni integrada.",
        ],
    },
    "situacion": {
        "derecha": [
            "El presente refleja {arquetipo}. Tu psique te muestra esta verdad ahora.",
        ],
        "invertida": [
            "En el presente, {arquetipo} aparece contraída: la energía existe pero no fluye libremente.",
        ],
    },
    "potencial": {
        "derecha": [
            "Lo que puede florecer se conecta con {arquetipo}. No es destino — es potencial real.",
        ],
        "invertida": [
            "El potencial de {arquetipo} aparece replegado. Hay un florecimiento que algo aún detiene.",
        ],
    },
    "presente": {
        "derecha": [
            "El presente te muestra {arquetipo}. Esta es la energía que domina tu momento actual.",
        ],
        "invertida": [
            "En el presente, {arquetipo} aparece en su cara oculta. Hay algo que no estás viendo.",
        ],
    },
    "sombra": {
        "directa": [
            "La sombra que confronta el presente es {arquetipo}. En Marsella, esta carta no 'bloquea' — muestra lo que la energía central aún no ha integrado.",
            "La carta que cruza al presente lleva la energía de {arquetipo}: es el complemento oscuro, lo que el presente necesita enfrentar para moverse.",
        ],
        "contraída": [
            "La sombra aparece con {arquetipo} contraída: hay algo que actúa por debajo de la situación visible, sin querer ser visto.",
        ],
        "derecha": [
            "La sombra que confronta el presente porta {arquetipo}. No es un obstáculo: es lo que la carta central no ha integrado todavía.",
        ],
        "invertida": [
            "La sombra lleva {arquetipo} contraída — trabajando desde lo oculto, difícil de reconocer directamente.",
        ],
    },
    "obstaculo": {
        "derecha": [
            "Lo que confronta al presente lleva la energía de {arquetipo}. La resistencia contiene su propia clave.",
        ],
        "invertida": [
            "La sombra de {arquetipo} actúa desde lo no visto. Lo que resiste también protege algo.",
        ],
    },
    "pasado": {
        "derecha": [
            "Tu pasado reciente trae la energía de {arquetipo}. Este patrón sigue activo en ti.",
        ],
        "invertida": [
            "En el pasado, {arquetipo} apareció de forma distorsionada. Hay una herida que sanar.",
        ],
    },
    "camino": {
        "directa": [
            "El camino que se abre porta la energía de {arquetipo}. No es predicción — es la dirección que la situación tiende a tomar si nada se interviene.",
            "La fuerza de {arquetipo} marca el camino abierto. La pregunta no es si ocurrirá — es qué parte de ti ya lo está viviendo.",
        ],
        "contraída": [
            "El camino aparece con {arquetipo} contraída: la dirección está, pero algo la estrecha. Hay un movimiento que aún no encuentra su forma.",
        ],
        "derecha": [
            "El camino que se abre está marcado por {arquetipo}. No es destino — es tendencia activa.",
        ],
        "invertida": [
            "El camino muestra {arquetipo} contraída: la dirección existe pero no fluye libremente.",
        ],
    },
    "futuro_cercano": {
        "derecha": [
            "Lo próximo está teñido de {arquetipo}. No es predicción — es la tendencia activa del patrón.",
        ],
        "invertida": [
            "El camino cercano porta {arquetipo} contraída: algo en la dirección no fluye aún.",
        ],
    },
    "meta": {
        "derecha": [
            "Tu meta consciente se alinea con {arquetipo}. Esto es lo que crees buscar.",
        ],
        "invertida": [
            "Lo que crees que buscas (meta) está invertido respecto a {arquetipo}. Quizás buscas fuera lo que está dentro.",
        ],
    },
    "resultado": {
        "derecha": [
            "El resultado potencial apunta a {arquetipo}. Si sigues este camino, esta energía se manifestará.",
        ],
        "invertida": [
            "El resultado potencial muestra {arquetipo} invertido: el camino tiene un giro inesperado esperándote.",
        ],
    },
    "unica": {
        "derecha": [
            "La carta que emergió es {arquetipo}. Una sola imagen contiene todo lo que necesitas ver ahora.",
            "El oráculo responde con {arquetipo}. Esta energía es tu espejo en este momento.",
        ],
        "invertida": [
            "La carta única aparece invertida: {arquetipo} te habla desde la sombra, desde lo que aún no has integrado.",
        ],
    },
    "fundamento": {
        "derecha": [
            "En la base inconsciente de tu pregunta yace {arquetipo}. Es el suelo sobre el que todo lo demás se sostiene.",
        ],
        "invertida": [
            "El fundamento muestra {arquetipo} invertido: hay algo oculto bajo la superficie que sostiene la situación.",
        ],
    },
    "consultante": {
        "derecha": [
            "En este momento, tú encarnas {arquetipo}. Esta es la energía que proyectas al mundo.",
        ],
        "invertida": [
            "La carta del consultante muestra {arquetipo} invertido: hay una brecha entre quien crees ser y quien eres.",
        ],
    },
    "influencias": {
        "derecha": [
            "Las fuerzas externas que actúan en tu situación traen {arquetipo}. El entorno resuena con este patrón.",
        ],
        "invertida": [
            "Las influencias externas muestran {arquetipo} invertido: hay presiones que no reconoces como tales.",
        ],
    },
    "esperanzas_miedos": {
        "derecha": [
            "Lo que simultáneamente deseas y temes se conecta con {arquetipo}. La ambivalencia misma es la clave.",
        ],
        "invertida": [
            "Tus esperanzas y miedos proyectan {arquetipo} invertido: lo que evitas puede ser lo que más necesitas.",
        ],
    },
    # Viaje del Héroe
    "mundo_ordinario": {
        "directa": ["Tu punto de partida real es {arquetipo}. No donde crees estar — donde realmente estás."],
        "derecha":  ["Tu punto de partida está marcado por {arquetipo}. Este es el suelo que conoces."],
    },
    "llamado": {
        "directa": ["{arquetipo} es la forma que tiene el llamado en tu vida ahora. La aventura ya te está convocando."],
        "derecha":  ["{arquetipo} es el llamado que sientes. La aventura tiene esta forma."],
    },
    "rechazo": {
        "directa": ["La resistencia al cambio lleva la energía de {arquetipo}. Todo héroe teme cruzar el umbral — incluso cuando lo desea."],
        "derecha":  ["La resistencia que encuentras es {arquetipo}. Todo héroe teme cruzar el umbral."],
    },
    "mentor": {
        "directa": ["{arquetipo} aparece como guía en este momento. La sabiduría que necesitas tiene esta forma."],
        "derecha":  ["{arquetipo} es la guía que aparece en tu camino. Escucha desde aquí."],
    },
    "cruce_umbral": {
        "directa": ["El primer paso hacia lo desconocido está marcado por {arquetipo}. Este es el umbral real."],
        "derecha":  ["El cruce hacia lo desconocido está marcado por {arquetipo}. Este es el primer gran paso."],
    },
    "pruebas": {
        "directa": ["Las pruebas que enfrentas en el camino traen {arquetipo}. Aliados y obstáculos son espejos del mismo patrón."],
        "derecha":  ["Las pruebas del camino traen {arquetipo}. Aliados y enemigos son espejos del mismo patrón."],
    },
    "caverna": {
        "directa": ["En el corazón del viaje, {arquetipo} espera. Esta es la prueba más profunda — la que no puede evitarse."],
        "derecha":  ["En lo más profundo de la prueba, {arquetipo} espera. Aquí está el corazón del viaje."],
    },
    "prueba_suprema": {
        "directa": ["La prueba definitiva encarna {arquetipo}. Todo lo vivido hasta aquí conduce a este momento."],
        "derecha":  ["La prueba definitiva encarna {arquetipo}. Todo lo vivido lleva a este momento."],
    },
    "recompensa": {
        "directa": ["Lo que obtienes al atravesar la caverna es {arquetipo}. No necesariamente lo que esperabas — lo que realmente te transforma."],
        "derecha":  ["El elixir que recibes es {arquetipo}. Esto es lo que ganaste al atravesar el umbral."],
    },
    "camino_regreso": {
        "directa": ["El retorno al mundo ordinario está marcado por {arquetipo}. Llevas algo nuevo que el mundo necesita."],
        "derecha":  ["El retorno está marcado por {arquetipo}. Llevas algo nuevo al mundo conocido."],
    },
    "resurreccion": {
        "directa": ["{arquetipo} es la transformación final — la última muerte y renacimiento antes de cruzar de vuelta."],
        "derecha":  ["{arquetipo} es la última transformación antes de regresar. El héroe renace aquí."],
    },
    "elixir": {
        "directa": ["Lo que traes de vuelta para tu mundo es {arquetipo}. Este es el regalo del viaje — lo que se transforma en servicio."],
        "derecha":  ["Lo que traes de vuelta es {arquetipo}. Esto es el regalo para tu mundo."],
    },
    # ── Fuerza y Flaqueza ─────────────────────────────────────────────────────
    "fuerza": {
        "directa": [
            "Tu recurso activo es {arquetipo}. No lo que aspiras a ser — lo que ya opera en ti y puedes usar ahora mismo.",
            "{arquetipo} es lo que ya tienes disponible. Esta energía no necesita ser desarrollada: necesita ser reconocida y desplegada.",
        ],
    },
    "flaqueza": {
        "directa": [
            "Lo que aún no integraste porta la energía de {arquetipo}. No es un defecto — es la parte de ti que tiene más para darte cuando se reconoce.",
            "{arquetipo} es la sombra que opera desde lo no visto. Nombrarla no la elimina: la transforma en recurso.",
        ],
    },
    # ── El Conflicto ─────────────────────────────────────────────────────────
    "tension": {
        "directa": [
            "La tensión que atraviesa esta situación porta {arquetipo}. No la bloquea ni la resuelve — la profundiza. Lee las dos cartas como un sistema.",
            "{arquetipo} es la fuerza que complica la situación. La tensión no es el problema — es lo que revela la verdadera estructura del momento.",
        ],
    },
    # ── La Duda ───────────────────────────────────────────────────────────────
    "consultante_d": {
        "directa": [
            "Tú en este momento de la duda encarnas {arquetipo}. Esta es la energía que eres mientras preguntas.",
            "{arquetipo} es quien pregunta ahora. La duda no es externa — viene de aquí, de esta energía que eres tú.",
        ],
    },
    "duda_a": {
        "directa": [
            "Una cara de la duda porta {arquetipo}. No es la opción correcta ni la incorrecta — es una energía real con su propia lógica.",
            "{arquetipo} es una de las fuerzas en tensión. Para verla bien, no la evalúes: observa qué describe en tu vida real.",
        ],
    },
    "duda_b": {
        "directa": [
            "La otra cara de la duda trae {arquetipo}. Tiene el mismo peso real que la primera — no se trata de elegir la mejor sino de ver ambas.",
            "{arquetipo} es la segunda energía en juego. Ninguna cara de la duda es superior: las dos revelan algo verdadero.",
        ],
    },
    "clave_d": {
        "directa": [
            "La clave para ver claramente es {arquetipo}. No dice qué elegir — muestra qué hay que entender antes de poder elegir.",
            "{arquetipo} es lo que la psique ofrece cuando deja de pelear con la duda. No es una respuesta: es una perspectiva.",
        ],
    },
    # ── La Liberación ────────────────────────────────────────────────────────
    "bloqueo": {
        "directa": [
            "Lo que te impide ser tú mismo en esta situación porta {arquetipo}. No es el obstáculo externo — es el patrón que se repite internamente.",
            "{arquetipo} es la fuerza que frena el movimiento. Nombrarlo con precisión es el primer paso de la liberación.",
        ],
    },
    "medio": {
        "directa": [
            "El medio por el que puede ocurrir la liberación es {arquetipo}. No el destino — el movimiento concreto posible.",
            "{arquetipo} es el puente entre el bloqueo y la acción. No lo busques fuera: ya está disponible.",
        ],
    },
    "accion": {
        "directa": [
            "La acción concreta que la liberación requiere porta {arquetipo}. No es una actitud — es un movimiento real.",
            "{arquetipo} es el gesto que transforma el medio en resultado. La liberación tiene una forma: esta.",
        ],
    },
    "transformacion": {
        "directa": [
            "La transformación que ese movimiento produce porta {arquetipo}. No es el destino — es lo que cambia en ti en el proceso.",
            "{arquetipo} es quien emerges al atravesar la acción. La transformación no es la meta: es el camino haciéndose visible.",
        ],
    },
    "destino": {
        "directa": [
            "El objetivo real de este proceso porta {arquetipo}. No lo que creías buscar — lo que la tirada completa apunta.",
            "{arquetipo} es lo que aparece cuando la liberación ocurre de verdad. Vale la pena verificar si eso es lo que realmente querías.",
        ],
    },
    # ── El Héroe (5) ─────────────────────────────────────────────────────────
    "partida": {
        "directa": [
            "El punto de partida real de este viaje es {arquetipo}. No dónde crees estar — dónde realmente estás.",
            "{arquetipo} es el suelo desde el que partes. Antes de mirar hacia la meta, vale la pena reconocer este punto de origen.",
        ],
    },
    "obstaculo_a": {
        "directa": [
            "El obstáculo exterior porta {arquetipo}. Lo que el mundo, las circunstancias o los otros ponen en el camino.",
            "{arquetipo} es la resistencia que viene de afuera. No es solo un impedimento — es también un espejo de lo que falta integrar.",
        ],
    },
    "obstaculo_b": {
        "directa": [
            "El obstáculo interior porta {arquetipo}. Lo que tú mismo pones en el camino sin darte cuenta.",
            "{arquetipo} es la resistencia que viene de adentro. Este es el obstáculo más difícil de ver — y el más poderoso cuando se reconoce.",
        ],
    },
    "clave_h": {
        "directa": [
            "La clave o aliado porta {arquetipo}. Puede leerse antes del obstáculo (cómo prepararse) o después (qué se aprende al atravesarlo).",
            "{arquetipo} es el recurso que el viaje te entrega. No siempre se ve antes de llegar al obstáculo — a veces solo se reconoce después.",
        ],
    },
    # ── El Mundo ─────────────────────────────────────────────────────────────
    "esencia": {
        "directa": [
            "Tu esencia central porta {arquetipo}. La energía que eres en el núcleo, independiente del contexto o el rol.",
            "{arquetipo} es quien eres cuando no estás actuando para nadie. Este es el centro desde el que se leen las otras cuatro cartas.",
        ],
    },
    "intelectual": {
        "directa": [
            "Tu vida intelectual porta {arquetipo}. Cómo piensas, qué parte de tu mente está activa o dormida en relación a la pregunta.",
            "{arquetipo} es la energía que gobierna tu pensamiento ahora. Observa si esa mente te sirve o te limita.",
        ],
    },
    "emocional": {
        "directa": [
            "Tu vida emocional porta {arquetipo}. Lo que fluye o se bloquea en el dominio del sentir.",
            "{arquetipo} es la energía que habita tu mundo afectivo. La carta no juzga — describe.",
        ],
    },
    "sexual_creativo": {
        "directa": [
            "Tu energía creativa y vital porta {arquetipo}. La libido en el sentido amplio: lo que creas, deseas, generas.",
            "{arquetipo} es la fuerza que anima tu deseo y tu creación. Observa si esa energía fluye o está contenida.",
        ],
    },
    "material": {
        "directa": [
            "Tu vida material porta {arquetipo}. Cómo habitas el mundo tangible — los recursos, el cuerpo, lo que tienes y lo que te falta.",
            "{arquetipo} es la energía que gobierna tu relación con lo concreto. El cuerpo, el dinero, el espacio que ocupas.",
        ],
    },
    # ── Yo Realizado ─────────────────────────────────────────────────────────
    "protagonista": {
        "directa": [
            "{arquetipo} es cómo te concives a ti mismo — no necesariamente quién eres, sino quién crees ser. La narrativa del yo.",
            "El protagonista porta {arquetipo}. Esta es la identidad que proyectas y desde la que actúas — consciente o no.",
        ],
    },
    "antagonista": {
        "directa": [
            "{arquetipo} es lo que rechazas de ti. No el enemigo — la energía de ti mismo que aún no integraste.",
            "El antagonista porta {arquetipo}. No es lo opuesto al protagonista: es su polaridad necesaria. Sin este, el protagonista no se completa.",
        ],
    },
    "mediador": {
        "directa": [
            "{arquetipo} es lo que ocurre entre el protagonista y el antagonista — el puente, la función que puede unir las dos polaridades.",
            "El mediador porta {arquetipo}. Esta carta no elige un bando: sostiene la tensión para que ambas energías puedan dialogar.",
        ],
    },
    "cometa_a": {
        "directa": [
            "{arquetipo} es lo que te nutre. Una energía que viene hacia ti y alimenta el proceso de realizarte.",
            "El Cometa A porta {arquetipo}. Lo que llega, lo que te sostiene, lo que aporta sin que tengas que buscarlo.",
        ],
    },
    "cometa_b": {
        "directa": [
            "{arquetipo} es lo que te expande — otra fuente de nutrición, en una dimensión diferente al primer cometa.",
            "El Cometa B porta {arquetipo}. Una segunda energía que te alimenta desde otro ángulo. Compara las dos: ¿en qué se complementan?",
        ],
    },
    "asteroide_a": {
        "directa": [
            "{arquetipo} es lo que te frena — la energía que ralentiza o dificulta el movimiento del protagonista.",
            "El Asteroide A porta {arquetipo}. No necesariamente algo externo: puede ser una parte de ti que actúa en contra del proceso.",
        ],
    },
    "asteroide_b": {
        "directa": [
            "{arquetipo} es lo que actúa en tu perjuicio — consciente o no. La segunda resistencia.",
            "El Asteroide B porta {arquetipo}. Compara con el primer asteroide: ¿actúan en la misma dirección o en ángulos diferentes?",
        ],
    },
    "resultado_a": {
        "directa": [
            "{arquetipo} es lo que emerge de la síntesis protagonista–mediador–antagonista. El primer resultado visible.",
            "El Resultado A porta {arquetipo}. Lo que comienza a manifestarse cuando la tensión entre el protagonista y el antagonista encuentra su mediador.",
        ],
    },
    "resultado_b": {
        "directa": [
            "{arquetipo} es la personalidad que puede nacer — quién puedes llegar a ser si todo el patrón se integra.",
            "El Resultado B porta {arquetipo}. No es un destino — es una posibilidad. El yo que emerge cuando todo el sistema se realiza.",
        ],
    },
    "secreto": {
        "directa": [
            "{arquetipo} es el secreto íntimo que rige todo desde lo invisible. El núcleo más profundo de la tirada.",
            "El Secreto porta {arquetipo}. Esta carta no se anuncia — opera silenciosamente debajo de todo lo demás. Ver esto puede cambiar la lectura completa.",
        ],
    },
}

# Cierre integrador para la tirada completa (lenguaje Jodorowsky)
CIERRES_TAROT = [
    "\n\nLa Raíz alimenta el Tallo, el Tallo sostiene la Flor. "
    "Estas tres cartas no describen tres momentos — describen un solo movimiento vivo. "
    "Lo que resuene en ti no es coincidencia: es reconocimiento.",

    "\n\nEl Tarot de Marsella no adivina: muestra el patrón que ya opera. "
    "Estas imágenes son un espejo, no una profecía. La pregunta que hiciste ya contenía su propia respuesta — "
    "las cartas solo te ayudaron a verla.",

    "\n\nCada carta habla con las demás. El significado no vive en ninguna imagen sola — "
    "vive en el diálogo entre ellas. Presta atención a lo que te incomoda: "
    "ahí suele estar lo que más necesitas ver.",
]


def generar_interpretacion_tarot(datos: dict) -> dict:
    """Genera interpretación terapéutica completa para una tirada de tarot."""
    ai_result = interpretar_tarot_ai(datos)
    if ai_result and ai_result.get("por_carta"):
        return {
            "texto_completo": ai_result.get("integracion", ""),
            "por_carta": ai_result["por_carta"],
            "fuente": "ai",
        }

    # Fallback simbólico
    cartas = datos["cartas"]
    por_carta = {}
    partes = []

    for carta in cartas:
        posicion_clave = carta.get("posicion_clave", "")
        posicion_label = carta.get("posicion", posicion_clave)
        estado = carta.get("estado", "directa")
        arquetipo = carta["arquetipo"]
        nombre = carta["nombre"]

        frases_pos = FRASES_POSICION_TAROT.get(
            posicion_clave,
            FRASES_POSICION_TAROT.get("tallo", FRASES_POSICION_TAROT.get("situacion"))
        )
        # Buscar clave de estado: directa → directa, contraída → contraída, caer en derecha/invertida si no existe
        frases_estado = (
            frases_pos.get(estado)
            or frases_pos.get("directa")
            or frases_pos.get("derecha")
            or ["La energía de {arquetipo} opera en esta posición."]
        )
        frase = random.choice(frases_estado).format(arquetipo=arquetipo)

        palo = carta.get("palo")
        elemento = carta.get("elemento")
        palo_info = ""
        if palo and elemento:
            palo_info = f" Al pertenecer al palo de {palo.capitalize()} ({elemento}), esta energía se expresa en el dominio de: {arquetipo}."

        texto_carta = f"**{nombre}** — {posicion_label}: {frase}{palo_info}"
        por_carta[posicion_clave] = texto_carta
        partes.append(texto_carta)

    texto_completo = _sintetizar_tirada(cartas, datos.get("pregunta", ""), datos.get("tipo_tirada", ""))

    return {
        "texto_completo": texto_completo,
        "por_carta": por_carta,
        "fuente": "estatico",
    }


def _sintetizar_tirada(cartas: list, pregunta: str, tipo_tirada: str) -> str:
    """Genera una lectura de integración que vincula las cartas entre sí y con la pregunta."""
    por_pos = {c.get("posicion_clave", ""): c for c in cartas}
    intro_pregunta = f"Ante «{pregunta}», " if pregunta.strip() else ""

    # ── Raíz–Tallo–Flor ──────────────────────────────────────────────────────
    if tipo_tirada == "tres_cartas" and all(k in por_pos for k in ("raiz", "tallo", "flor")):
        raiz = por_pos["raiz"]
        tallo = por_pos["tallo"]
        flor = por_pos["flor"]

        raiz_estado = "pero sin ser reconocida — opera desde la sombra" if raiz.get("estado", "directa") == "contraída" else "activa y visible"
        tallo_estado = "replegada, sin flujo libre" if tallo.get("estado", "directa") == "contraída" else "en movimiento"
        flor_estado = "bloqueado todavía" if flor.get("estado", "directa") == "contraída" else "disponible si la raíz se nombra"

        sintesis = (
            f"{intro_pregunta}las tres cartas revelan un solo arco:\n\n"
            f"**{raiz['nombre']}** en la raíz opera {raiz_estado}. "
            f"Es la fuerza que origina la situación que preguntas — haya o no conciencia de ella.\n\n"
            f"**{tallo['nombre']}** en el presente muestra cómo esa raíz se expresa hoy ({tallo_estado}). "
            f"No es una situación separada: es la raíz manifestándose.\n\n"
            f"**{flor['nombre']}** señala el potencial ({flor_estado}). "
            f"No es destino — es lo que puede nacer cuando la energía de la raíz deja de operar en la sombra.\n\n"
            f"La pregunta que atraviesa las tres: ¿qué de lo que origina esta situación "
            f"sigue sin ser nombrado en voz alta?"
        )
        return sintesis + random.choice(CIERRES_TAROT)

    # ── Una carta ────────────────────────────────────────────────────────────
    if tipo_tirada == "un_arcano" and len(cartas) == 1:
        c = cartas[0]
        return (
            f"{intro_pregunta}el oráculo responde con una sola imagen: **{c['nombre']}**.\n\n"
            f"Una carta no da una respuesta — da un espejo. Lo que ves en ella ya vive en ti.\n\n"
            f"La pregunta que abre la imagen: ¿en qué parte de tu vida está actuando esta energía "
            f"sin haber sido nombrada?"
        ) + random.choice(CIERRES_TAROT)

    # ── Fuerza y Flaqueza ────────────────────────────────────────────────────
    if tipo_tirada == "fuerza_flaqueza" and all(k in por_pos for k in ("fuerza", "flaqueza")):
        f_ = por_pos["fuerza"]
        fl = por_pos["flaqueza"]
        return (
            f"{intro_pregunta}las dos cartas no se oponen — se complementan:\n\n"
            f"**{f_['nombre']}** como recurso: la energía que ya opera en ti y puedes desplegar ahora mismo. "
            f"No necesita ser construida — necesita ser reconocida.\n\n"
            f"**{fl['nombre']}** como sombra: la energía que aún no integraste. La flaqueza no es ausencia de fuerza — "
            f"es fuerza que todavía no encontró su forma consciente.\n\n"
            f"La pregunta que une las dos: ¿cómo se alimentan mutuamente estas dos energías "
            f"en lo que estás viviendo ahora?"
        ) + random.choice(CIERRES_TAROT)

    # ── El Conflicto ─────────────────────────────────────────────────────────
    if tipo_tirada == "el_conflicto" and all(k in por_pos for k in ("situacion", "tension")):
        sit = por_pos["situacion"]
        ten = por_pos["tension"]
        return (
            f"{intro_pregunta}las dos cartas forman un sistema:\n\n"
            f"**{sit['nombre']}** es la situación o el deseo presente — la energía que está en primer plano.\n\n"
            f"**{ten['nombre']}** no bloquea esa situación: la atraviesa, la complica, la profundiza. "
            f"La tensión no es el problema — es lo que revela la verdadera estructura del momento.\n\n"
            f"¿Qué está diciendo la tensión sobre la situación que todavía no habías escuchado?"
        ) + random.choice(CIERRES_TAROT)

    # ── La Duda ──────────────────────────────────────────────────────────────
    if tipo_tirada == "la_duda" and "consultante_d" in por_pos:
        cons = por_pos["consultante_d"]
        da   = por_pos.get("duda_a")
        db   = por_pos.get("duda_b")
        clave = por_pos.get("clave_d")
        partes = [f"{intro_pregunta}la tirada muestra la estructura de la duda:\n"]
        partes.append(f"**{cons['nombre']}** eres tú en este momento — la energía que encarnas mientras preguntas.")
        if da and db:
            partes.append(
                f"Las dos caras de la duda son **{da['nombre']}** y **{db['nombre']}**. "
                f"No son la opción correcta y la incorrecta — son dos energías reales con su propia lógica. "
                f"La duda no se resuelve eligiendo la mejor: se resuelve entendiendo qué describe cada una."
            )
        if clave:
            partes.append(
                f"**{clave['nombre']}** como clave no dice qué elegir — muestra qué hay que ver antes de poder elegir."
            )
        partes.append("\n¿Cuál de las dos caras de la duda describe algo verdadero sobre tu situación que todavía no nombraste?")
        return "\n\n".join(partes) + random.choice(CIERRES_TAROT)

    # ── La Liberación ────────────────────────────────────────────────────────
    if tipo_tirada == "la_liberacion" and "bloqueo" in por_pos:
        bl = por_pos["bloqueo"]
        me = por_pos.get("medio")
        ac = por_pos.get("accion")
        tr = por_pos.get("transformacion")
        de = por_pos.get("destino")
        partes = [f"{intro_pregunta}las cinco cartas trazan un arco de movimiento:\n"]
        partes.append(f"**{bl['nombre']}** como bloqueo: el patrón que se repite y frena el movimiento real.")
        if me:
            partes.append(f"**{me['nombre']}** como medio: la forma en que la liberación puede ocurrir — no el destino, el movimiento posible.")
        if ac:
            partes.append(f"**{ac['nombre']}** como acción: el gesto concreto que convierte el medio en resultado.")
        if tr:
            partes.append(f"**{tr['nombre']}** como transformación: quién emerges al atravesar esa acción.")
        if de:
            partes.append(f"**{de['nombre']}** como destino: el objetivo real — lo que aparece cuando la liberación ocurre de verdad.")
        partes.append(
            "\nCada carta transforma la anterior. Este no es un listado de consejos — "
            "es una historia de movimiento. ¿En cuál de estas cinco etapas estás realmente ahora?"
        )
        return "\n\n".join(partes) + random.choice(CIERRES_TAROT)

    # ── El Héroe (5) ─────────────────────────────────────────────────────────
    if tipo_tirada == "el_heroe_5" and "partida" in por_pos:
        pa = por_pos["partida"]
        me = por_pos.get("meta")
        oa = por_pos.get("obstaculo_a")
        ob = por_pos.get("obstaculo_b")
        cl = por_pos.get("clave_h")
        partes = [f"{intro_pregunta}el viaje tiene esta forma:\n"]
        partes.append(f"**{pa['nombre']}** es el punto de partida real — el suelo desde el que el héroe se mueve.")
        if me:
            partes.append(f"**{me['nombre']}** es la meta — hacia dónde se dirige la energía.")
        if oa and ob:
            partes.append(
                f"Los dos obstáculos forman un par: **{oa['nombre']}** (exterior — lo que el mundo pone) "
                f"y **{ob['nombre']}** (interior — lo que el propio héroe pone). "
                f"Leídos juntos, revelan la naturaleza real de la resistencia."
            )
        if cl:
            partes.append(
                f"**{cl['nombre']}** como clave puede leerse antes del obstáculo (cómo prepararse) "
                f"o después (qué se aprende al atravesarlo)."
            )
        partes.append("\n¿Cuál de los dos obstáculos — el exterior o el interior — es en realidad el más difícil de atravesar?")
        return "\n\n".join(partes) + random.choice(CIERRES_TAROT)

    # ── El Mundo ─────────────────────────────────────────────────────────────
    if tipo_tirada == "el_mundo" and "esencia" in por_pos:
        es = por_pos["esencia"]
        dims = {
            "intelectual":     ("águila", "cómo piensas"),
            "emocional":       ("ángel",  "cómo sientes"),
            "sexual_creativo": ("león",   "tu energía vital y creadora"),
            "material":        ("buey",   "cómo habitas el mundo"),
        }
        partes = [
            f"{intro_pregunta}las cinco cartas dibujan el mapa completo del ser:\n",
            f"**{es['nombre']}** en el centro es tu esencia — quien eres cuando no estás actuando para nadie.",
        ]
        for key, (figura, desc) in dims.items():
            if key in por_pos:
                partes.append(f"**{por_pos[key]['nombre']}** ({figura}) describe {desc}.")
        partes.append(
            "\nEl patrón que importa: ¿qué dimensión está en tensión con la esencia? "
            "¿Cuál fluye con facilidad? Ahí está lo que la tirada quiere que veas."
        )
        return "\n\n".join(partes) + random.choice(CIERRES_TAROT)

    # ── Yo Realizado ─────────────────────────────────────────────────────────
    if tipo_tirada == "yo_realizado" and "protagonista" in por_pos:
        prot = por_pos["protagonista"]
        anta = por_pos.get("antagonista")
        medi = por_pos.get("mediador")
        sec  = por_pos.get("secreto")
        rb   = por_pos.get("resultado_b")
        partes = [f"{intro_pregunta}el Yo Realizado revela la estructura de la psique en este momento:\n"]
        partes.append(
            f"**{prot['nombre']}** como protagonista: cómo te concives. "
            + (f"**{anta['nombre']}** como antagonista: lo que rechazas de ti mismo." if anta else "")
        )
        if medi:
            partes.append(f"**{medi['nombre']}** como mediador: la función que puede unir esas dos polaridades.")
        if sec:
            partes.append(
                f"**{sec['nombre']}** en el secreto íntimo: el núcleo que rige todo desde lo invisible. "
                f"Este es el dato central de la tirada — todo lo demás orbita alrededor de aquí."
            )
        if rb:
            partes.append(f"**{rb['nombre']}** como resultado final: quien puedes llegar a ser si todo el patrón se integra.")
        partes.append(
            "\nLa pregunta que abre la tirada entera: ¿qué parte del antagonista "
            "— lo que rechazas de ti — tiene en realidad la clave de lo que más necesitas?"
        )
        return "\n\n".join(partes) + random.choice(CIERRES_TAROT)

    # ── Viaje del Héroe ───────────────────────────────────────────────────────
    if tipo_tirada == "viaje_heroe" and "caverna" in por_pos:
        cav = por_pos["caverna"]
        ps  = por_pos.get("prueba_suprema")
        eli = por_pos.get("elixir")
        lla = por_pos.get("llamado")
        partes = [f"{intro_pregunta}el Viaje del Héroe despliega el arco completo:\n"]
        if lla:
            partes.append(f"El viaje comienza con **{lla['nombre']}** como llamado — la forma que tiene la aventura en tu vida.")
        partes.append(
            f"El corazón del viaje: **{cav['nombre']}** en la Caverna — "
            + (f"y **{ps['nombre']}** como prueba suprema. " if ps else ". ")
            + "Estas dos etapas son el núcleo real — todo lo anterior llevaba aquí, todo lo que sigue nace desde aquí."
        )
        if eli:
            partes.append(
                f"**{eli['nombre']}** como elixir: no lo que se ganó — lo que se soltó. "
                f"El regalo del viaje raramente es lo que se esperaba al partir."
            )
        partes.append(
            "\n¿Qué murió simbólicamente en la Caverna? ¿Quién regresa que no es el mismo que partió?"
        )
        return "\n\n".join(partes) + random.choice(CIERRES_TAROT)

    # ── Cruz de 5 ─────────────────────────────────────────────────────────────
    if tipo_tirada == "cruz_normal" and "presente" in por_pos:
        presente = por_pos["presente"]
        sombra = por_pos.get("sombra") or por_pos.get("obstaculo")
        pasado = por_pos.get("pasado")
        camino = por_pos.get("camino") or por_pos.get("futuro_cercano")
        fundamento = por_pos.get("fundamento")

        partes_cruz = [f"{intro_pregunta}la Cruz revela la estructura completa del momento:\n"]
        if fundamento:
            partes_cruz.append(f"**{fundamento['nombre']}** como fundamento inconsciente sostiene todo lo demás.")
        partes_cruz.append(f"**{presente['nombre']}** en el centro es la energía que domina ahora mismo.")
        if sombra:
            partes_cruz.append(f"**{sombra['nombre']}** como sombra no se opone al presente — completa lo que el presente no puede ver solo.")
        if pasado:
            partes_cruz.append(f"**{pasado['nombre']}** en el pasado aún resuena en la situación actual.")
        if camino:
            partes_cruz.append(f"**{camino['nombre']}** indica hacia dónde se mueve la energía si el patrón continúa.")

        partes_cruz.append("\nEl patrón completo: lo que el pasado dejó, lo que la sombra revela, y lo que el camino señala son una misma fuerza vista desde ángulos distintos.")
        return "\n\n".join(partes_cruz) + random.choice(CIERRES_TAROT)

    # ── Genérico (Cruz Celta, Viaje del Héroe, 1 carta, otros) ───────────────
    nombres = " · ".join(f"**{c['nombre']}**" for c in cartas)
    estado_general = "contraída" if sum(1 for c in cartas if c.get("estado", "directa") == "contraída") > len(cartas) / 2 else "activa"
    tension = "La energía general de la tirada está replegada — hay más actuando desde lo inconsciente que desde lo visible." \
        if estado_general == "contraída" else \
        "La energía general de la tirada está en movimiento — lo que se ve y lo que opera coinciden más de lo usual."

    return (
        f"{intro_pregunta}las cartas {nombres} trazan el patrón de la situación.\n\n"
        f"{tension}\n\n"
        f"El hilo que conecta todas las posiciones: cada carta no describe un aspecto aislado — "
        f"describe el mismo territorio desde una perspectiva distinta. "
        f"Presta atención a las que generan más resistencia interior: ahí suele estar el centro del patrón."
    ) + random.choice(CIERRES_TAROT)


# ═══════════════════════════════════════════════════
# INTERPRETACIONES DE I CHING (Taoísta)
# ═══════════════════════════════════════════════════

REFLEXIONES_I_CHING = [
    "El I Ching no predice el futuro — revela el patrón del momento presente. "
    "Este hexagrama es un espejo de tu situación actual, no una sentencia. "
    "La sabiduría taoísta enseña que todo fluye: lo que hoy es desafío, mañana será enseñanza. "
    "Tu pregunta ha encontrado su eco en este antiguo símbolo. Escucha lo que tiene para decirte.",

    "El Libro de las Mutaciones habla en el lenguaje del cambio constante. "
    "Este hexagrama refleja la energía que rodea tu pregunta. No es destino — es tendencia. "
    "El Tao no fuerza, no empuja, no predice. Simplemente muestra el río en este instante. "
    "Tú decides cómo navegar sus aguas.",

    "La respuesta del I Ching no es una orden, es una invitación a la reflexión. "
    "Este hexagrama te muestra dónde estás en el gran ciclo de la transformación. "
    "Lo que parece obstáculo puede ser el camino. Lo que parece pérdida puede ser liberación. "
    "El sabio taoísta observa, acepta y fluye.",
]

REFLEXIONES_LINEAS_MOVILES = [
    "Las líneas móviles indican puntos de transformación activa en tu situación. "
    "Son las semillas del cambio, los lugares donde la energía está en movimiento. "
    "Presta especial atención a estas áreas: son donde tu acción consciente puede marcar la diferencia.",

    "Las líneas en movimiento revelan que tu situación no es estática. "
    "Hay fuerzas transformándose bajo la superficie. El I Ching te señala estos puntos "
    "para que puedas trabajar con el cambio, no en su contra.",
]

REFLEXIONES_HEXAGRAMA_SECUNDARIO = [
    "El hexagrama secundario muestra hacia dónde se dirige esta energía si permites que la transformación ocurra. "
    "No es un destino fijo — es el siguiente paso natural del proceso que ya está en marcha.",

    "La transformación del hexagrama primario al secundario revela el arco de tu situación. "
    "Muestra cómo lo que es puede convertirse en lo que será, si sigues el flujo natural del cambio.",
]


def generar_interpretacion_iching(datos: dict) -> dict:
    """Genera interpretación taoísta completa para una lectura de I Ching."""
    ai_texto = interpretar_iching_ai(datos)
    if ai_texto:
        return {"texto_completo": ai_texto, "fuente": "ai"}

    # Static fallback — conecta el hexagrama directamente con la pregunta
    hp = datos.get("hexagrama_primario", {})
    hs = datos.get("hexagrama_secundario")
    lineas_moviles = datos.get("lineas_moviles", {})
    pregunta = datos.get("pregunta", "").strip()
    nombre = hp.get("nombre", "")
    numero = hp.get("numero", "")
    dictamen = hp.get("dictamen", "")
    imagen = hp.get("imagen", "")
    partes = []

    # Primer párrafo: hexagrama + pregunta directamente conectados
    if dictamen and pregunta:
        partes.append(
            f"Ante la pregunta «{pregunta}», el I Ching responde con {nombre} (#{numero}).\n\n"
            f"Su dictamen: \"{dictamen}\"\n\n"
            f"No leas esto como un consejo. Lee qué principio describe la pregunta misma — "
            f"qué patrón de fuerza está activo en la situación que preguntas."
        )
    elif dictamen:
        partes.append(
            f"{nombre} (#{numero}) porta un dictamen preciso: \"{dictamen}\"\n\n"
            f"El I Ching no habla del futuro; habla del patrón presente con una claridad "
            f"que el pensamiento analítico raramente alcanza."
        )

    if imagen:
        partes.append(
            f"La imagen: \"{imagen}\"\n\n"
            f"Obsérvala literalmente — ¿qué movimiento, qué fuerza, qué relación describe? "
            f"Eso mismo está ocurriendo en el territorio que tu pregunta toca."
        )

    if lineas_moviles:
        partes.append(random.choice(REFLEXIONES_LINEAS_MOVILES))

    if hs:
        hs_nombre = hs.get("nombre", "")
        hs_dictamen = hs.get("dictamen", "")
        if hs_nombre:
            partes.append(
                f"Las líneas móviles transforman el hexagrama en {hs_nombre}. "
                f"\"{hs_dictamen}\" — "
                f"esta es la dirección que toma la energía si la transformación ocurre."
            )

    if not partes:
        partes.append(random.choice(REFLEXIONES_I_CHING))

    return {
        "texto_completo": "\n\n".join(partes),
        "fuente": "estatico",
    }


# ═══════════════════════════════════════════════════
# INTERPRETACIONES DE ORÁCULO FRACTAL — sistema de 33 cartas (Yuda, 2023)
# ═══════════════════════════════════════════════════

PREFIJOS_INVERTIDA = [
    "La carta aparece invertida: su energía se expresa desde la sombra, desde lo que aún no ha sido integrado. ",
    "Invertida, esta carta no niega su mensaje — lo profundiza hacia lo no visible. ",
    "En posición invertida, la fuerza de esta carta actúa desde el inconsciente. ",
]

CIERRES_FRACTAL = [
    "\n\nEl Oráculo Fractal no predice — refleja. Cada carta es un espejo; lo que ves en ella, ya vive en ti.",
    "\n\nEsta carta no llega por azar: la geometría de tu pregunta la convocó. Confía en lo que despierta.",
    "\n\nEl sistema fractal de la psique se repite en todas las escalas. Lo que esta carta señala hoy tiene ecos en tu pasado y en tu potencial.",
    "\n\nLos oráculos no hablan del destino sino del momento presente vista desde una conciencia más amplia.",
]

REFLEXIONES_DAAT = [
    "Daat es el abismo. No hay interpretación posible para lo que no puede ser dicho. Solo hay presencia.",
    "Cuando el oráculo responde con el vacío, el vacío es la respuesta. Permanece en la pregunta.",
    "Daat marca el umbral de lo indecible. Aquí el lenguaje se detiene y comienza la experiencia directa.",
]


def generar_interpretacion_fractal(datos: dict) -> dict:
    """Genera interpretación para la carta del Oráculo Fractal."""
    carta = datos.get("carta", {})
    es_especial = carta.get("es_especial", False)
    invertida = carta.get("invertida", False)
    tipo = carta.get("tipo", "arcano")
    verbo = carta.get("verbo", "")
    descripcion = carta.get("descripcion_breve", "")
    nombre = carta.get("nombre_arcano", "")

    # Carta especial: Daat — no AI, solo silencio poético
    if es_especial:
        texto = random.choice(REFLEXIONES_DAAT)
        return {"texto_completo": texto, "fuente": "especial"}

    # Try AI first
    ai_texto = interpretar_fractal_ai(datos)
    if ai_texto:
        return {"texto_completo": ai_texto, "fuente": "ai"}

    # Static fallback — usa descripcion_larga (no repetir descripcion_breve que ya está en la carta)
    descripcion_larga = carta.get("descripcion_larga", "").strip()
    pregunta = datos.get("pregunta", "").strip()
    partes = []

    if tipo == "arcano":
        texto_base = descripcion_larga or descripcion
        sefirot_nombre = carta.get("sefirot_nombre", "")
        contexto = sefirot_nombre if sefirot_nombre else verbo
        partes.append(
            f"El arquetipo que responde a esta pregunta es **{nombre}** — el principio del {verbo.lower()}.\n\n{texto_base}"
        )
    else:
        sefirot_nombre = carta.get("sefirot_nombre", nombre)
        texto_base = descripcion_larga or descripcion
        partes.append(f"**{sefirot_nombre}**\n\n{texto_base}")

    if invertida:
        partes.append(random.choice(PREFIJOS_INVERTIDA))

    if pregunta:
        partes.append(
            f"Ante la pregunta «{pregunta}»: observa en qué parte de tu vida esta energía está presente "
            f"pero no está siendo reconocida o expresada."
        )

    partes.append(random.choice(CIERRES_FRACTAL))

    return {
        "texto_completo": "\n\n".join(partes),
        "fuente": "estatico",
    }
