"""
Anamnesis estructurada por signos — adaptación digital de los Cuatro Exámenes
(MTC, Wen/Wang/Qie-zhen) y el interrogatorio ayurvédico (Roga Pariksha).

Diseño clave del rediseño: en vez de preguntas abiertas emocionales, se
recolectan SIGNOS OBJETIVOS con opciones cerradas y lenguaje simple, aptas para
usuarios que no conocen su propio cuerpo. Cada opción mapea a `ejes` MTC
(ver ejes.py) y, opcionalmente, a `dx` (pesos directos hacia diagnósticos de
otros paradigmas en catalogo_otros.py).

Estructura de pregunta:
    {
      "id": "G01", "signo": "termorregulacion",
      "pregunta": "...", "ayuda": "...",
      "tipo": "radio" | "checkbox",
      "opciones": [
        {"valor": "...", "etiqueta": "...", "ejes": {axis: peso}, "dx": {id: peso}},
      ],
    }

Los pesos negativos en `ejes` son DISCRIMINANTES (restan): p.ej. "sin sed"
resta al eje de Calor. Sin ellos no habría diagnóstico diferencial real.

Fase 1 implementa el método MTC completo + módulo de piel. Ayurveda (doshas,
Agni, Prakriti) entra en Fase 2 con sus propios ejes.
"""

# ─────────────────────────────────────────────────────────────
# TRIAJE — Sistemas / zonas (paso 1). Filtra qué patrones son candidatos.
# ─────────────────────────────────────────────────────────────
SISTEMAS = [
    {"id": "piel",         "nombre": "Piel",                    "icono": "🩹",
     "keywords": ["dermatitis", "eczema", "eccema", "picazón", "picor", "urticaria", "acné", "acne", "psoriasis", "piel", "sarpullido", "roncha", "erupción", "grano"]},
    {"id": "digestivo",    "nombre": "Digestión y vientre",     "icono": "🌀",
     "keywords": ["digestión", "digestion", "estómago", "estomago", "intestino", "colon", "acidez", "gases", "hinchazón", "estreñimiento", "diarrea", "náusea", "nausea", "reflujo"]},
    {"id": "dolor",        "nombre": "Dolor muscular o articular", "icono": "🦴",
     "keywords": ["dolor", "contractura", "lumbar", "espalda", "cuello", "articulación", "articular", "rodilla", "hombro", "muscular", "artritis"]},
    {"id": "respiratorio", "nombre": "Respiración y garganta",   "icono": "🫁",
     "keywords": ["respiración", "respiracion", "asma", "tos", "garganta", "alergia", "resfrío", "resfriado", "congestión", "bronquitis", "sinusitis"]},
    {"id": "cabeza",       "nombre": "Cabeza y sentidos",        "icono": "🧠",
     "keywords": ["cabeza", "cefalea", "migraña", "migrana", "mareo", "vértigo", "vertigo", "acúfeno", "tinnitus", "vista", "oído", "oido"]},
    {"id": "animo",        "nombre": "Ánimo, sueño y energía",   "icono": "🌙",
     "keywords": ["ansiedad", "estrés", "estres", "depresión", "insomnio", "sueño", "cansancio", "fatiga", "agotamiento", "ánimo", "animo", "tristeza", "irritable", "nervios"]},
    {"id": "gineco",       "nombre": "Ciclo y hormonas",         "icono": "🌸",
     "keywords": ["ciclo", "menstruación", "menstruacion", "regla", "menopausia", "hormona", "fertilidad", "ovario", "útero", "spm", "premenstrual"]},
    {"id": "otro",         "nombre": "Otro / no estoy seguro",   "icono": "❓",
     "keywords": []},
]

SISTEMAS_BY_ID = {s["id"]: s for s in SISTEMAS}


# ─────────────────────────────────────────────────────────────
# PASO 1 — Roga Pariksha (contexto de la molestia)
# ─────────────────────────────────────────────────────────────
ROGA_PARIKSHA = [
    {
        "id": "R01", "signo": "nidana",
        "pregunta": "¿Qué crees que lo desencadenó?",
        "ayuda": "Nidana: la causa. Puedes marcar más de una.",
        "tipo": "checkbox",
        "opciones": [
            {"valor": "alimento",   "etiqueta": "Algo que comí o bebí",                "ejes": {"humedad": 1}},
            {"valor": "clima",      "etiqueta": "Un cambio de clima o estación",       "ejes": {"viento": 1}},
            {"valor": "emocion",    "etiqueta": "Una emoción o un evento fuerte",      "ejes": {"qi_zhi": 2, "higado": 1}},
            {"valor": "esfuerzo",   "etiqueta": "Un esfuerzo físico o golpe",          "ejes": {"estasis": 2}},
            {"valor": "no_se",      "etiqueta": "No lo sé",                            "ejes": {}},
        ],
    },
    {
        "id": "R02", "signo": "upashaya_alivia",
        "pregunta": "¿Qué lo alivia?",
        "ayuda": "Upashaya: el mejor diferencial rápido. Marca lo que aplique.",
        "tipo": "checkbox",
        "opciones": [
            {"valor": "calor",      "etiqueta": "El calor (abrigo, bolsa caliente)",   "ejes": {"termico": -2}},
            {"valor": "frio",       "etiqueta": "El frío (fresco, agua fría)",         "ejes": {"termico": 2}},
            {"valor": "presion",    "etiqueta": "Presionar o apretar la zona",         "ejes": {"plenitud": -2}},
            {"valor": "movimiento", "etiqueta": "Moverme o caminar",                   "ejes": {"qi_zhi": 2, "estasis": 1}},
            {"valor": "reposo",     "etiqueta": "El reposo, quedarme quieto",          "ejes": {"plenitud": 1}},
            {"valor": "comer",      "etiqueta": "Comer algo",                          "ejes": {"plenitud": -1, "bazo": 1}},
            {"valor": "nada",       "etiqueta": "Nada en particular",                  "ejes": {}},
        ],
    },
    {
        "id": "R03", "signo": "upashaya_empeora",
        "pregunta": "¿Qué lo empeora?",
        "ayuda": "Marca lo que aplique.",
        "tipo": "checkbox",
        "opciones": [
            {"valor": "calor",      "etiqueta": "El calor o el abrigo",                "ejes": {"termico": 2}},
            {"valor": "frio",       "etiqueta": "El frío",                             "ejes": {"termico": -2}},
            {"valor": "presion",    "etiqueta": "Que me toquen o presionen la zona",   "ejes": {"plenitud": 2}},
            {"valor": "estres",     "etiqueta": "El estrés o las emociones",           "ejes": {"higado": 1, "qi_zhi": 2}},
            {"valor": "noche",      "etiqueta": "La noche",                            "ejes": {"yin_def": 1, "estasis": 1}},
            {"valor": "humedad",    "etiqueta": "La humedad o los días lluviosos",     "ejes": {"humedad": 2}},
            {"valor": "nada",       "etiqueta": "Nada en particular",                  "ejes": {}},
        ],
    },
]


# ─────────────────────────────────────────────────────────────
# PASO 2 — Interrogatorio general (Wen-zhen 问 / Shi Wen, Manual 2.1-2.7)
# ─────────────────────────────────────────────────────────────
MODULO_GENERAL = [
    {
        "id": "G01", "signo": "termorregulacion",
        "pregunta": "Comparado con la gente a tu alrededor, ¿sueles sentir…?",
        "ayuda": "Piensa en cómo te abrigas o si buscas la sombra.",
        "tipo": "radio",
        "opciones": [
            {"valor": "friolento",    "etiqueta": "Más frío: me abrigo más que el resto",          "ejes": {"termico": -2, "yang_def": 2, "plenitud": -1}},
            {"valor": "caluroso",     "etiqueta": "Más calor: destapo, busco el fresco",            "ejes": {"termico": 2, "plenitud": 1}},
            {"valor": "calor_tarde",  "etiqueta": "Calor por las tardes/noches, palmas y plantas",  "ejes": {"termico": 1, "yin_def": 2}},
            {"valor": "normal",       "etiqueta": "Normal, sin diferencia clara",                   "ejes": {}},
        ],
    },
    {
        "id": "G02", "signo": "sudor",
        "pregunta": "¿Cómo es tu sudoración?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "espontaneo",  "etiqueta": "Sudo con facilidad de día, sin esfuerzo",  "ejes": {"qi_def": 2, "plenitud": -1}},
            {"valor": "nocturno",    "etiqueta": "Sudo de noche o de madrugada",             "ejes": {"yin_def": 2, "termico": 1}},
            {"valor": "ausente",     "etiqueta": "Casi no sudo, aunque haga calor",          "ejes": {"termico": -1, "profundidad": 1}},
            {"valor": "normal",      "etiqueta": "Normal",                                   "ejes": {}},
        ],
    },
    {
        "id": "G03", "signo": "sed",
        "pregunta": "¿Cómo es tu sed?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "sed_fria",    "etiqueta": "Mucha sed, prefiero agua fría",              "ejes": {"termico": 2, "plenitud": 1}},
            {"valor": "boca_seca",   "etiqueta": "Boca seca (sobre todo de noche), a sorbos",  "ejes": {"yin_def": 2, "sequedad": 1}},
            {"valor": "sin_sed",     "etiqueta": "Poca sed, no me apetece beber",              "ejes": {"termico": -2}},
            {"valor": "normal",      "etiqueta": "Normal",                                     "ejes": {}},
        ],
    },
    {
        "id": "G04", "signo": "apetito",
        "pregunta": "¿Cómo es tu apetito y tu digestión?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "voraz_acidez",  "etiqueta": "Hambre voraz, acidez o ardor",              "ejes": {"estomago": 2, "termico": 1, "plenitud": 1}},
            {"valor": "poco_pesadez",  "etiqueta": "Poco apetito, pesadez después de comer",    "ejes": {"bazo": 2, "qi_def": 2, "humedad": 1, "plenitud": -1}},
            {"valor": "variable",      "etiqueta": "Varía con mi ánimo, con distensión y gases", "ejes": {"higado": 2, "qi_zhi": 2}},
            {"valor": "normal",        "etiqueta": "Normal",                                    "ejes": {}},
        ],
    },
    {
        "id": "G05", "signo": "heces",
        "pregunta": "¿Cómo son tus deposiciones?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "secas",       "etiqueta": "Secas y duras, me cuesta",           "ejes": {"sequedad": 2, "termico": 1, "ig": 2}},
            {"valor": "blandas",     "etiqueta": "Blandas, pastosas o diarrea",        "ejes": {"bazo": 2, "humedad": 1, "termico": -1, "yang_def": 1}},
            {"valor": "ardor",       "etiqueta": "Con urgencia y ardor al evacuar",    "ejes": {"termico": 2, "humedad": 1, "ig": 1}},
            {"valor": "alterna",     "etiqueta": "Alterna entre duras y blandas",      "ejes": {"higado": 1, "qi_zhi": 1}},
            {"valor": "normal",      "etiqueta": "Normal",                             "ejes": {}},
        ],
    },
    {
        "id": "G06", "signo": "orina",
        "pregunta": "¿Cómo es tu orina?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "clara",       "etiqueta": "Clara y abundante",           "ejes": {"termico": -2, "yang_def": 1}},
            {"valor": "oscura",      "etiqueta": "Oscura y escasa",             "ejes": {"termico": 2}},
            {"valor": "ardor",       "etiqueta": "Con ardor o molestia",        "ejes": {"humedad": 2, "termico": 1}},
            {"valor": "normal",      "etiqueta": "Normal",                      "ejes": {}},
        ],
    },
    {
        "id": "G07", "signo": "sueno",
        "pregunta": "¿Cómo es tu sueño?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "cuesta",      "etiqueta": "Me cuesta dormirme, la mente no para",     "ejes": {"corazon": 2, "termico": 1, "plenitud": 1}},
            {"valor": "madrugada",   "etiqueta": "Me despierto en la madrugada (1-3 am)",    "ejes": {"higado": 2, "qi_zhi": 1}},
            {"valor": "ligero_calor","etiqueta": "Sueño ligero, me despierto con calor",     "ejes": {"yin_def": 2, "termico": 1}},
            {"valor": "excesivo",    "etiqueta": "Duermo mucho y me cuesta despertar",       "ejes": {"humedad": 2, "qi_def": 1, "yang_def": 1}},
            {"valor": "bien",        "etiqueta": "Duermo bien",                              "ejes": {}},
        ],
    },
    {
        "id": "G08", "signo": "energia",
        "pregunta": "¿Cómo es tu energía durante el día?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "baja_manana", "etiqueta": "Baja por la mañana, me cuesta arrancar",   "ejes": {"qi_def": 2, "bazo": 1, "yang_def": 1}},
            {"valor": "cae_tarde",   "etiqueta": "Bien al principio, cae por la tarde",       "ejes": {"yin_def": 1, "qi_def": 1}},
            {"valor": "agotamiento", "etiqueta": "Agotamiento constante, profundo",           "ejes": {"qi_def": 2, "yang_def": 1, "plenitud": -1}},
            {"valor": "normal",      "etiqueta": "Normal",                                    "ejes": {}},
        ],
    },
    {
        "id": "G09", "signo": "emocion_organo",
        "pregunta": "¿Qué emociones sientes con más frecuencia últimamente?",
        "ayuda": "Cada emoción afecta un órgano (Manual 1.4B). Marca las que apliquen.",
        "tipo": "checkbox",
        "opciones": [
            {"valor": "irritabilidad", "etiqueta": "Irritabilidad, rabia o frustración",  "ejes": {"higado": 2, "qi_zhi": 1}},
            {"valor": "preocupacion",  "etiqueta": "Preocupación, le doy muchas vueltas",  "ejes": {"bazo": 2}},
            {"valor": "tristeza",      "etiqueta": "Tristeza o pena",                      "ejes": {"pulmon": 2}},
            {"valor": "miedo",         "etiqueta": "Miedo o inseguridad",                  "ejes": {"rinon": 2}},
            {"valor": "ansiedad",      "etiqueta": "Ansiedad, agitación",                  "ejes": {"corazon": 1, "termico": 1}},
            {"valor": "ninguna",       "etiqueta": "Ninguna en particular",               "ejes": {}},
        ],
    },
    {
        "id": "G10", "signo": "clima",
        "pregunta": "¿Qué tipo de clima te sienta peor?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "viento",  "etiqueta": "El viento o los cambios bruscos",  "ejes": {"viento": 2}},
            {"valor": "frio",    "etiqueta": "El frío",                          "ejes": {"termico": -2, "yang_def": 1}},
            {"valor": "humedad", "etiqueta": "La humedad",                       "ejes": {"humedad": 2}},
            {"valor": "calor",   "etiqueta": "El calor",                         "ejes": {"termico": 2}},
            {"valor": "seco",    "etiqueta": "El clima seco",                    "ejes": {"sequedad": 2, "yin_def": 1}},
            {"valor": "ninguno", "etiqueta": "Ninguno en particular",           "ejes": {}},
        ],
    },
    {
        "id": "G11", "signo": "cabeza",
        "pregunta": "Si tienes dolor de cabeza o mareos, ¿dónde/cómo?",
        "ayuda": "La localización orienta al órgano (Manual 2.2).",
        "tipo": "radio",
        "opciones": [
            {"valor": "frontal",     "etiqueta": "En la frente",                       "ejes": {"estomago": 1}},
            {"valor": "sienes",      "etiqueta": "En las sienes o los lados",          "ejes": {"higado": 2}},
            {"valor": "nuca",        "etiqueta": "En la nuca o la parte de atrás",     "ejes": {"rinon": 1, "viento": 1}},
            {"valor": "pesadez",     "etiqueta": "Toda la cabeza, con pesadez",        "ejes": {"humedad": 2, "tan": 1}},
            {"valor": "mareo_vista", "etiqueta": "Mareo con visión borrosa",           "ejes": {"xue_def": 2}},
            {"valor": "no",          "etiqueta": "No tengo",                           "ejes": {}},
        ],
    },
]


# ─────────────────────────────────────────────────────────────
# PASO 3 (a) — Auto-observación guiada (Wang-zhen / Darshana, Manual 3.2-3.3)
# La lengua alimenta `termico_lengua` (arbitra contradicciones, Manual 5.4).
# ─────────────────────────────────────────────────────────────
OBSERVACION = [
    {
        "id": "O01", "signo": "lengua_color",
        "pregunta": "Mírate la lengua al espejo con luz natural. ¿De qué color es el cuerpo?",
        "ayuda": "El cuerpo, no la capa de encima. Sin comer ni beber nada de color antes.",
        "tipo": "radio", "imagenes": True,
        "opciones": [
            {"valor": "palida",      "etiqueta": "Pálida (rosa muy claro)",         "img": "lengua_palida",     "ejes": {"termico_lengua": -1, "qi_def": 1, "xue_def": 1}},
            {"valor": "rosada",      "etiqueta": "Rosada (color sano)",             "img": "lengua_rosada",     "ejes": {}},
            {"valor": "roja",        "etiqueta": "Roja",                            "img": "lengua_roja",       "ejes": {"termico_lengua": 2}},
            {"valor": "roja_bordes", "etiqueta": "Roja sobre todo en los bordes",   "img": "lengua_bordes",     "ejes": {"termico_lengua": 1, "higado": 2}},
            {"valor": "roja_punta",  "etiqueta": "Roja sobre todo en la punta",     "img": "lengua_punta",      "ejes": {"termico_lengua": 1, "corazon": 2}},
            {"valor": "purpura",     "etiqueta": "Morada o violácea",               "img": "lengua_purpura",    "ejes": {"estasis": 2}},
        ],
    },
    {
        "id": "O02", "signo": "lengua_saburra",
        "pregunta": "¿Cómo es la capa (saburra) sobre la lengua?",
        "ayuda": "",
        "tipo": "radio", "imagenes": True,
        "opciones": [
            {"valor": "blanca_fina",      "etiqueta": "Blanca y fina",                    "img": "sab_blanca_fina",  "ejes": {}},
            {"valor": "blanca_gruesa",    "etiqueta": "Blanca y gruesa",                  "img": "sab_blanca_gruesa","ejes": {"humedad": 1, "termico_lengua": -1}},
            {"valor": "amarilla",         "etiqueta": "Amarilla",                         "img": "sab_amarilla",     "ejes": {"termico_lengua": 2}},
            {"valor": "amarilla_grasa",   "etiqueta": "Amarilla y grasienta/pegajosa",    "img": "sab_amarilla_grasa","ejes": {"humedad": 2, "termico_lengua": 1}},
            {"valor": "ausente",          "etiqueta": "Casi sin capa, lengua 'pelada'",   "img": "sab_ausente",      "ejes": {"yin_def": 2}},
            {"valor": "granos_rojos",     "etiqueta": "Con puntos o granos rojos",        "img": "sab_granos",       "ejes": {"calor_sangre": 2, "termico_lengua": 1}},
        ],
    },
    {
        "id": "O03", "signo": "lengua_forma",
        "pregunta": "¿Cómo es la forma de la lengua?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "hinchada",    "etiqueta": "Hinchada, con marcas de los dientes en los bordes",  "ejes": {"bazo": 1, "humedad": 1, "qi_def": 1}},
            {"valor": "delgada",     "etiqueta": "Delgada, seca o agrietada",                          "ejes": {"yin_def": 1, "xue_def": 1, "sequedad": 1}},
            {"valor": "normal",      "etiqueta": "Normal",                                             "ejes": {}},
        ],
    },
    {
        "id": "O04", "signo": "tez",
        "pregunta": "¿Cómo describes el color y aspecto de tu cara?",
        "ayuda": "Manual 3.1: el color facial orienta el patrón.",
        "tipo": "radio",
        "opciones": [
            {"valor": "palida",      "etiqueta": "Pálida o apagada",                  "ejes": {"qi_def": 1, "xue_def": 1}},
            {"valor": "rojiza",      "etiqueta": "Rojiza o con rubor",                "ejes": {"termico": 1}},
            {"valor": "amarillenta", "etiqueta": "Amarillenta o cetrina",             "ejes": {"humedad": 1, "bazo": 1}},
            {"valor": "oscura",      "etiqueta": "Oscura, con ojeras marcadas",       "ejes": {"estasis": 1, "rinon": 1}},
            {"valor": "normal",      "etiqueta": "Normal, con brillo",                "ejes": {}},
        ],
    },
    {
        "id": "O05", "signo": "pulso",
        "pregunta": "Si te tomas el pulso en reposo, ¿cómo lo notas? (opcional)",
        "ayuda": "El pulso fino requiere años de práctica; esto es solo orientativo.",
        "tipo": "radio",
        "opciones": [
            {"valor": "rapido",   "etiqueta": "Rápido",                 "ejes": {"termico": 1}},
            {"valor": "lento",    "etiqueta": "Lento",                  "ejes": {"termico": -1}},
            {"valor": "irregular","etiqueta": "Irregular o saltón",     "ejes": {"corazon": 1}},
            {"valor": "no_se",    "etiqueta": "Normal / no sé tomarlo", "ejes": {}},
        ],
    },
]


# ─────────────────────────────────────────────────────────────
# PASO 3 (b) — Módulos específicos por sistema. Fase 1: piel.
# ─────────────────────────────────────────────────────────────
MODULOS_ESPECIFICOS = {
    "piel": [
        {
            "id": "P01", "signo": "lesion_aspecto",
            "pregunta": "¿Cómo es el aspecto de la lesión de piel?",
            "ayuda": "",
            "tipo": "radio",
            "opciones": [
                {"valor": "roja_caliente",  "etiqueta": "Roja y caliente al tacto",            "ejes": {"termico": 2, "calor_sangre": 1, "pulmon": 1}},
                {"valor": "seca_descama",   "etiqueta": "Seca y descamativa (se pela)",        "ejes": {"sequedad": 2, "xue_def": 2}},
                {"valor": "vesiculas",      "etiqueta": "Con vesículas o supura líquido",      "ejes": {"humedad": 3, "termico": 1}},
                {"valor": "palida",         "etiqueta": "Pálida, sin mucho color",             "ejes": {"xue_def": 1, "termico": -1}},
                {"valor": "pus",            "etiqueta": "Con pus o costra amarilla",           "ejes": {"humedad": 2, "termico": 2}},
            ],
        },
        {
            "id": "P02", "signo": "picor",
            "pregunta": "¿Cómo es el picor?",
            "ayuda": "El picor que se mueve señala Viento (Manual 5.3C).",
            "tipo": "radio",
            "opciones": [
                {"valor": "migratorio", "etiqueta": "Intenso y cambia de lugar",     "ejes": {"viento": 3}},
                {"valor": "fijo",       "etiqueta": "Siempre en la misma zona",      "ejes": {"estasis": 1}},
                {"valor": "nocturno",   "etiqueta": "Peor de noche",                 "ejes": {"xue_def": 2, "calor_sangre": 1}},
                {"valor": "no_pica",    "etiqueta": "No pica",                       "ejes": {"viento": -1}},
            ],
        },
        {
            "id": "P03", "signo": "agravantes_piel",
            "pregunta": "¿Qué empeora la piel? (marca lo que aplique)",
            "ayuda": "",
            "tipo": "checkbox",
            "opciones": [
                {"valor": "calor",     "etiqueta": "El calor o el abrigo",                  "ejes": {"termico": 2}},
                {"valor": "estres",    "etiqueta": "El estrés",                             "ejes": {"higado": 1, "qi_zhi": 1}},
                {"valor": "alimentos", "etiqueta": "Ciertos alimentos (picante, alcohol, mariscos)", "ejes": {"termico": 1, "humedad": 1}},
                {"valor": "contacto",  "etiqueta": "El contacto (jabón, telas, productos)", "ejes": {"viento": 1}, "dx": {"D09": 0}},
                {"valor": "nada",      "etiqueta": "Nada claro",                            "ejes": {}},
            ],
        },
        {
            "id": "P04", "signo": "localizacion_piel",
            "pregunta": "¿Dónde se localiza principalmente? (marca lo que aplique)",
            "ayuda": "",
            "tipo": "checkbox",
            "opciones": [
                {"valor": "cara_cuello", "etiqueta": "Cara o cuello",                   "ejes": {"pulmon": 1, "termico": 1}},
                {"valor": "pliegues",    "etiqueta": "Pliegues (codos, rodillas, ingle)","ejes": {"humedad": 1}},
                {"valor": "manos",       "etiqueta": "Manos",                           "ejes": {}},
                {"valor": "tronco",      "etiqueta": "Tronco o espalda",                "ejes": {}},
                {"valor": "extendido",   "etiqueta": "Extendido por todo el cuerpo",    "ejes": {"viento": 1}},
            ],
        },
        {
            "id": "P05", "signo": "evolucion_piel",
            "pregunta": "¿Cómo evoluciona?",
            "ayuda": "",
            "tipo": "radio",
            "opciones": [
                {"valor": "brotes",     "etiqueta": "Va y viene en brotes",         "ejes": {"viento": 1, "profundidad": 1}},
                {"valor": "constante",  "etiqueta": "Está siempre presente",        "ejes": {"profundidad": -1}},
                {"valor": "progresivo", "etiqueta": "Empeora poco a poco",          "ejes": {}},
            ],
        },
        {
            "id": "P06", "signo": "humedad_piel",
            "pregunta": "En general, tu piel es más bien…",
            "ayuda": "",
            "tipo": "radio",
            "opciones": [
                {"valor": "seca",   "etiqueta": "Muy seca",   "ejes": {"sequedad": 2, "xue_def": 1}},
                {"valor": "normal", "etiqueta": "Normal",     "ejes": {}},
                {"valor": "grasa",  "etiqueta": "Grasa",      "ejes": {"humedad": 1}},
            ],
        },
    ],
}


# ─────────────────────────────────────────────────────────────
# PASO 3 (c) — Contexto emocional-familiar (rescatado del banco anterior).
# Alimenta diagnósticos de otros paradigmas (PSI/SOC/VIB) vía `dx`.
# Los ids D## corresponden a catalogo_otros.DIAGNOSIS_OTROS.
# ─────────────────────────────────────────────────────────────
MODULO_EMOCIONAL = [
    {
        "id": "E01", "signo": "cambios_vida",
        "pregunta": "¿Ha habido cambios importantes en tu vida antes de que empezara? (marca lo que aplique)",
        "ayuda": "",
        "tipo": "checkbox",
        "opciones": [
            {"valor": "perdida_trabajo",  "etiqueta": "Pérdida o cambio de trabajo",        "ejes": {}, "dx": {"D17": 1, "D23": 1}},
            {"valor": "separacion",       "etiqueta": "Separación o conflicto de pareja",    "ejes": {}, "dx": {"D04": 2}},
            {"valor": "duelo",            "etiqueta": "Pérdida de un ser querido",           "ejes": {"pulmon": 1}, "dx": {"D04": 2}},
            {"valor": "conflicto_fam",    "etiqueta": "Conflictos familiares sostenidos",    "ejes": {}, "dx": {"D11": 1, "D04": 1}},
            {"valor": "ninguno",          "etiqueta": "No, nada significativo",              "ejes": {}, "dx": {}},
        ],
    },
    {
        "id": "E02", "signo": "emocion_sintoma",
        "pregunta": "¿Qué emoción sientes al pensar en tu molestia?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "miedo",    "etiqueta": "Miedo o angustia",       "ejes": {"rinon": 1}, "dx": {"D16": 2, "D13": 1}},
            {"valor": "tristeza", "etiqueta": "Tristeza",               "ejes": {"pulmon": 1}, "dx": {"D04": 1}},
            {"valor": "rabia",    "etiqueta": "Rabia o frustración",    "ejes": {"higado": 1, "qi_zhi": 1}, "dx": {}},
            {"valor": "vacio",    "etiqueta": "Vacío o desvalorización","ejes": {}, "dx": {"D09": 2}},
            {"valor": "nada",     "etiqueta": "Nada en particular",     "ejes": {}, "dx": {}},
        ],
    },
    {
        "id": "E03", "signo": "funcion_sintoma",
        "pregunta": "¿Sientes que el síntoma cumple alguna función, te protege o te impide algo?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "si",       "etiqueta": "Sí, veo una función",   "ejes": {}, "dx": {"D04": 1, "D20": 1}},
            {"valor": "tal_vez",  "etiqueta": "Tal vez, lo sospecho",  "ejes": {}, "dx": {"D20": 1}},
            {"valor": "no",       "etiqueta": "No lo veo así",         "ejes": {}, "dx": {}},
        ],
    },
    {
        "id": "E04", "signo": "patron_familiar",
        "pregunta": "¿Notas patrones (enfermedades, historias) que se repiten en tu familia?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "si_claros",   "etiqueta": "Sí, bastante claros",       "ejes": {}, "dx": {"D11": 2}},
            {"valor": "similitudes", "etiqueta": "Algunas similitudes",       "ejes": {}, "dx": {"D11": 1}},
            {"valor": "no",          "etiqueta": "No los veo",                "ejes": {}, "dx": {}},
        ],
    },
    {
        "id": "E05", "signo": "merecimiento",
        "pregunta": "¿Sientes que mereces sanar y estar bien?",
        "ayuda": "",
        "tipo": "radio",
        "opciones": [
            {"valor": "si",       "etiqueta": "Sí, completamente",             "ejes": {}, "dx": {}},
            {"valor": "cuesta",   "etiqueta": "A veces me cuesta creerlo",     "ejes": {}, "dx": {"D09": 1, "D23": 1}},
            {"valor": "no",       "etiqueta": "Honestamente, no lo siento",    "ejes": {}, "dx": {"D09": 2, "D23": 1}},
        ],
    },
]


# ─────────────────────────────────────────────────────────────
# Índice de todas las preguntas por id (para persistir texto humano y validar).
# ─────────────────────────────────────────────────────────────
def _index_preguntas():
    idx = {}
    grupos = [ROGA_PARIKSHA, MODULO_GENERAL, OBSERVACION, MODULO_EMOCIONAL]
    for g in grupos:
        for q in g:
            idx[q["id"]] = q
    for _sis, preguntas in MODULOS_ESPECIFICOS.items():
        for q in preguntas:
            idx[q["id"]] = q
    return idx

PREGUNTAS_BY_ID = _index_preguntas()
