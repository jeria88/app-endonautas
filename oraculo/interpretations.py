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
    "origen": {
        "derecha": [
            "Tu historia comienza con {arquetipo}. Este arquetipo te acompaña desde hace tiempo, moldeando tu manera de ver el mundo.",
            "El origen de tu situación actual se conecta con {arquetipo}. Tu inconsciente ha estado procesando este patrón.",
            "En la raíz de lo que consultas, {arquetipo} emerge como fuerza formativa de tu experiencia.",
        ],
        "invertida": [
            "El arquetipo de {arquetipo} aparece bloqueado en tu historia. Hay algo del pasado que aún no has integrado.",
            "La energía de {arquetipo} se manifiesta de forma invertida: en lugar de impulsarte, te ha detenido.",
            "Tu relación con {arquetipo} en el origen está distorsionada. Quizás has negado esta parte de ti.",
        ],
    },
    "situacion": {
        "derecha": [
            "En tu presente, {arquetipo} te muestra dónde estás parado. Tu inconsciente te invita a reconocer este patrón.",
            "La situación actual refleja {arquetipo}. Estás proyectando esta energía en tu vida cotidiana.",
            "Aquí y ahora, {arquetipo} domina el escenario. Tu psique te está mostrando esta verdad.",
        ],
        "invertida": [
            "En el presente, {arquetipo} aparece invertido: la energía está ahí pero no la reconoces.",
            "Tu situación actual muestra {arquetipo} en su sombra. Hay una parte de ti que resiste esta verdad.",
            "El arquetipo de {arquetipo} en tu presente te pide que mires lo que estás evitando.",
        ],
    },
    "potencial": {
        "derecha": [
            "El potencial que emerge es {arquetipo}. Si integras esta energía, tu camino se abre.",
            "Lo que puede florecer en ti está conectado con {arquetipo}. Tu inconsciente te señala esta dirección.",
            "El futuro como posibilidad te muestra {arquetipo}. No es destino, es tendencia arquetípica.",
        ],
        "invertida": [
            "El potencial de {arquetipo} aparece invertido: hay una oportunidad que estás dejando pasar.",
            "Lo que podría ser se ve bloqueado por la sombra de {arquetipo}. Presta atención a esta resistencia.",
            "Tu potencial conectado con {arquetipo} necesita ser reclamado. La inversión sugiere trabajo interior pendiente.",
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
    "obstaculo": {
        "derecha": [
            "El obstáculo que enfrentas se conecta con {arquetipo}. Tu sombra te está protegiendo de algo.",
        ],
        "invertida": [
            "Lo que te bloquea es la sombra de {arquetipo}. La resistencia misma contiene la clave.",
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
    "futuro_cercano": {
        "derecha": [
            "Lo que se acerca en tu horizonte está teñido de {arquetipo}. No es predicción, es tendencia.",
        ],
        "invertida": [
            "El futuro cercano muestra {arquetipo} invertido: prepárate para una sorpresa que desafía tus expectativas.",
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
        "derecha": ["Tu punto de partida está marcado por {arquetipo}. Este es el suelo que conoces."],
        "invertida": ["El mundo que dejaste atrás tiene {arquetipo} en su sombra. Hay algo que aún no soltaste."],
    },
    "llamado": {
        "derecha": ["{arquetipo} es el llamado que sientes. La aventura tiene esta forma."],
        "invertida": ["El llamado llega distorsionado como {arquetipo}. Puede ser difícil reconocerlo."],
    },
    "rechazo": {
        "derecha": ["La resistencia que encuentras es {arquetipo}. Todo héroe teme cruzar el umbral."],
        "invertida": ["Tu rechazo al llamado tiene la sombra de {arquetipo}. ¿Qué te detiene realmente?"],
    },
    "mentor": {
        "derecha": ["{arquetipo} es la guía que aparece en tu camino. Escucha desde aquí."],
        "invertida": ["El mentor aparece como {arquetipo} invertido: la guía puede venir de donde menos esperas."],
    },
    "cruce_umbral": {
        "derecha": ["El cruce hacia lo desconocido está marcado por {arquetipo}. Este es el primer gran paso."],
        "invertida": ["El umbral muestra {arquetipo} invertido: hay un precio oculto en este cruce."],
    },
    "pruebas": {
        "derecha": ["Las pruebas del camino traen {arquetipo}. Aliados y enemigos son espejos del mismo patrón."],
        "invertida": ["Las pruebas revelan {arquetipo} en su cara oscura. La dificultad es la enseñanza."],
    },
    "caverna": {
        "derecha": ["En lo más profundo de la prueba, {arquetipo} espera. Aquí está el corazón del viaje."],
        "invertida": ["La caverna muestra {arquetipo} invertido: el mayor obstáculo es interior."],
    },
    "prueba_suprema": {
        "derecha": ["La prueba definitiva encarna {arquetipo}. Todo lo vivido lleva a este momento."],
        "invertida": ["La prueba suprema revela {arquetipo} en su sombra máxima. La muerte simbólica es real."],
    },
    "recompensa": {
        "derecha": ["El elixir que recibes es {arquetipo}. Esto es lo que ganaste al atravesar el umbral."],
        "invertida": ["La recompensa aparece como {arquetipo} invertido: puede no ser lo que esperabas."],
    },
    "camino_regreso": {
        "derecha": ["El retorno está marcado por {arquetipo}. Llevas algo nuevo al mundo conocido."],
        "invertida": ["El camino de regreso muestra {arquetipo} invertido: hay una tentación de no volver."],
    },
    "resurreccion": {
        "derecha": ["{arquetipo} es la última transformación antes de regresar. El héroe renace aquí."],
        "invertida": ["La resurrección muestra {arquetipo} en su sombra: algo viejo aún se aferra a ti."],
    },
    "elixir": {
        "derecha": ["Lo que traes de vuelta es {arquetipo}. Esto es el regalo para tu mundo."],
        "invertida": ["El elixir aparece como {arquetipo} invertido: el regalo puede ser difícil de dar o recibir."],
    },
}

# Cierre integrador para la tirada completa
CIERRES_TAROT = [
    "\n\nEstas tres cartas forman un diálogo entre tu pasado, tu presente y tu potencial. "
    "No te dicen qué va a pasar — te muestran qué arquetipos están activos en tu psique ahora mismo. "
    "La pregunta no es '¿qué me depara el futuro?', sino '¿qué parte de mí necesita atención en este momento?'",

    "\n\nLa tirada revela un patrón arquetípico en movimiento. Tu inconsciente, a través de estas imágenes simbólicas, "
    "te está mostrando una narrativa interna. No es adivinación — es espejo. Lo que resuene, quédate con ello. "
    "Lo que no, déjalo pasar como una nube en el cielo de tu consciencia.",

    "\n\nEstas cartas no predicen: reflejan. El tarot terapéutico funciona como un espejo del inconsciente. "
    "Lo que ves en ellas es una proyección de tu mundo interior. La pregunta que hiciste ya contiene su propia respuesta — "
    "estas imágenes solo te ayudan a verla desde otro ángulo.",
]


def generar_interpretacion_tarot(datos: dict) -> dict:
    """Genera interpretación terapéutica completa para una tirada de tarot."""
    # Try AI first
    ai_texto = interpretar_tarot_ai(datos)
    if ai_texto:
        return {"texto_completo": ai_texto, "por_carta": {}, "fuente": "ai"}

    # Static fallback
    cartas = datos["cartas"]
    por_carta = {}
    partes = []

    for carta in cartas:
        posicion = carta["posicion"]
        estado = carta["estado"]
        arquetipo = carta["arquetipo"]
        nombre = carta["nombre"]

        frases_pos = FRASES_POSICION_TAROT.get(posicion, FRASES_POSICION_TAROT["situacion"])
        frases_estado = frases_pos.get(estado, frases_pos["derecha"])
        frase = random.choice(frases_estado).format(arquetipo=arquetipo)

        palo_info = ""
        if carta.get("palo"):
            palo_info = f" Al pertenecer al palo de {carta['palo']}, esta energía se manifiesta en el ámbito de {carta.get('arquetipo', 'tu vida')}."

        texto_carta = f"**{nombre}** ({estado}): {frase}{palo_info}"
        por_carta[posicion] = texto_carta
        partes.append(texto_carta)

    cierre = random.choice(CIERRES_TAROT)
    texto_completo = "\n\n".join(partes) + cierre

    return {
        "texto_completo": texto_completo,
        "por_carta": por_carta,
        "fuente": "estatico",
    }


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

    # Static fallback — usa los datos concretos del hexagrama, no frases genéricas
    hp = datos.get("hexagrama_primario", {})
    hs = datos.get("hexagrama_secundario")
    lineas_moviles = datos.get("lineas_moviles", {})
    nombre = hp.get("nombre", "")
    numero = hp.get("numero", "")
    dictamen = hp.get("dictamen", "")
    imagen = hp.get("imagen", "")
    partes = []

    if dictamen:
        partes.append(
            f"{nombre} (#{numero}) porta un dictamen preciso: \"{dictamen}\"\n\n"
            f"Este no es un texto abstracto — es una descripción de la fuerza que "
            f"opera en tu situación en este momento. El I Ching no habla del futuro; "
            f"habla del patrón presente con una claridad que el pensamiento analítico "
            f"raramente alcanza."
        )

    if imagen:
        partes.append(
            f"La imagen asociada — \"{imagen}\" — muestra el principio en su forma natural, "
            f"antes de que la mente lo interprete. Obsérvala literalmente: ¿qué movimiento, "
            f"qué fuerza, qué relación describe? Eso mismo está ocurriendo en tu vida ahora."
        )

    if lineas_moviles:
        partes.append(random.choice(REFLEXIONES_LINEAS_MOVILES))

    if hs:
        hs_nombre = hs.get("nombre", "")
        hs_dictamen = hs.get("dictamen", "")
        if hs_nombre:
            partes.append(
                f"Las líneas en movimiento transforman el hexagrama en {hs_nombre}. "
                f"Su dictamen dice: \"{hs_dictamen}\" "
                f"Esta es la dirección hacia donde se mueve la energía si permites que el cambio ocurra."
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

    # Try AI first — la plantilla ya muestra descripcion_breve, solo retornar lectura
    ai_texto = interpretar_fractal_ai(datos)
    if ai_texto:
        return {"texto_completo": ai_texto, "fuente": "ai"}

    # Static fallback
    partes = []
    if tipo == "arcano":
        partes.append(f"**{verbo}**\n\n{descripcion}")
    else:
        sefirot_nombre = carta.get("sefirot_nombre", nombre)
        partes.append(f"**{sefirot_nombre}**\n\n{descripcion}")

    if invertida:
        partes.append(random.choice(PREFIJOS_INVERTIDA))

    partes.append(random.choice(CIERRES_FRACTAL))

    return {
        "texto_completo": "\n\n".join(partes),
        "fuente": "estatico",
    }
