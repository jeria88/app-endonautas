"""
Constants for consulta_integral app.

This module contains all the structured data for the integral therapy
consultation wizard: frameworks (dimensions), techniques, question bank,
diagnosis catalog, and keyword mappings.

Everything is defined here as Python data structures so the AI can ONLY
select from these pre-defined items — no free-text generation allowed.
"""

# ─────────────────────────────────────────────────────────────
# 1. FRAMEWORKS (Dimensions) and their TECHNIQUES
# ─────────────────────────────────────────────────────────────

FRAMEWORKS_AND_TECHNIQUES = {
    "Biomédico (Occidental)": {
        "framework_code": "BIO",
        "descripcion": "Abordaje basado en evidencia científica occidental: anatomía, fisiología, bioquímica y farmacología.",
        "tecnicas": {
            "BIO-ALO": {
                "nombre": "Medicina Alopática / Farmacología",
                "descripcion": "Abordaje químico-fisiológico mediante fármacos y procedimientos médicos convencionales.",
            },
            "BIO-NUT": {
                "nombre": "Nutrición Clínica y Ortomolecular",
                "descripcion": "Abordaje bioquímico-nutricional: micronutrientes, suplementación y dieta terapéutica.",
            },
            "BIO-FIS": {
                "nombre": "Fisioterapia / Rehabilitación",
                "descripcion": "Abordaje mecánico-funcional: movimiento, terapia manual y ejercicio terapéutico.",
            },
            "BIO-REF": {
                "nombre": "Reflexología Podal y Manual",
                "descripcion": "Estimulación de zonas reflejas en pies y manos que corresponden a órganos y sistemas corporales, facilitando la autorregulación.",
            },
        },
    },
    "Medicina Tradicional China (MTC)": {
        "framework_code": "MTC",
        "descripcion": "Sistema médico milenario basado en el flujo de Qi, los meridianos y el balance Yin-Yang.",
        "tecnicas": {
            "MTC-ACU": {
                "nombre": "Acupuntura / Moxibustión",
                "descripcion": "Regulación de canales energéticos mediante agujas y calor en puntos específicos.",
            },
            "MTC-FIT": {
                "nombre": "Fitoterapia China",
                "descripcion": "Balance de Yín-Yang mediante fórmulas herbales tradicionales chinas.",
            },
            "MTC-TUI": {
                "nombre": "Tui Na / Chi Kung",
                "descripcion": "Movimiento y manipulación energética: masaje terapéutico y ejercicios de respiración consciente.",
            },
            "MTC-AUR": {
                "nombre": "Auriculoterapia / Auriculopuntura",
                "descripcion": "Estimulación de puntos reflejos en el pabellón auricular que mapean el sistema nervioso y todos los órganos del cuerpo.",
            },
        },
    },
    "Ayurveda": {
        "framework_code": "AYU",
        "descripcion": "Ciencia de la vida de origen védico: balance de doshas (Vata, Pitta, Kapha) para salud integral.",
        "tecnicas": {
            "AYU-DIE": {
                "nombre": "Dietoterapia Ayurvédica",
                "descripcion": "Balance de Doshas mediante alimentación específica según constitución individual.",
            },
            "AYU-PAN": {
                "nombre": "Panchakarma y Terapias de Limpieza",
                "descripcion": "Purificación física y energética mediante procedimientos de desintoxicación profunda.",
            },
            "AYU-YOG": {
                "nombre": "Yoga / Pranayama",
                "descripcion": "Armonización mente-cuerpo-respiración mediante posturas y técnicas de respiración.",
            },
        },
    },
    "Vibracional / Energético Sutil": {
        "framework_code": "VIB",
        "descripcion": "Terapias que trabajan con campos energéticos sutiles, frecuencias y resonancia.",
        "tecnicas": {
            "VIB-REI": {
                "nombre": "Reiki / Toque Terapéutico",
                "descripcion": "Canalización de energía universal a través de las manos para restaurar el flujo vital.",
            },
            "VIB-RES": {
                "nombre": "Resonance Repatterning",
                "descripcion": "Cambio de patrones resonantes limitantes para alinearse con frecuencias de bienestar.",
            },
            "VIB-SON": {
                "nombre": "Terapia de Sonido / Radiestesia",
                "descripcion": "Armonización por frecuencias: cuencos, diapasones y detección de desequilibrios energéticos.",
            },
        },
    },
    "Psicosomático (Mente-Cuerpo-Emoción)": {
        "framework_code": "PSI",
        "descripcion": "Abordaje de la relación entre emociones, sistema nervioso y manifestaciones corporales.",
        "tecnicas": {
            "PSI-PNI": {
                "nombre": "Psiconeuroinmunología (PNI) / Biofeedback",
                "descripcion": "Eje mente-sistema inmune: regulación del estrés y retroalimentación biológica.",
            },
            "PSI-BIO": {
                "nombre": "Bioneuroemoción / Biodescodificación",
                "descripcion": "Sentido biológico de los síntomas: conflictos emocionales que se expresan en el cuerpo.",
            },
            "PSI-SOM": {
                "nombre": "Somatic Experiencing / Focusing",
                "descripcion": "Liberación de traumas almacenados en el cuerpo mediante atención somática.",
            },
        },
    },
    "Socio-familiar (Contexto y Sistemas)": {
        "framework_code": "SOC",
        "descripcion": "Abordaje del contexto relacional, familiar y social como factor de salud y enfermedad.",
        "tecnicas": {
            "SOC-CON": {
                "nombre": "Constelaciones Familiares",
                "descripcion": "Órdenes del amor y lealtades invisibles que afectan la salud del sistema familiar.",
            },
            "SOC-GEN": {
                "nombre": "Genograma / Terapia Narrativa Familiar",
                "descripcion": "Patrones transgeneracionales y narrativas familiares que condicionan la salud.",
            },
            "SOC-ANT": {
                "nombre": "Antropología Médica / Ecología Social",
                "descripcion": "Entorno cultural, comunitario y social como determinante de salud.",
            },
        },
    },
}

# ─────────────────────────────────────────────────────────────
# 2. FLAT TECHNIQUE LIST (for easy lookups)
# ─────────────────────────────────────────────────────────────

def get_all_tecnicas():
    """Returns a flat dict of all techniques: {codigo_interno: {nombre, marco, framework_code}}"""
    result = {}
    for marco_name, marco_data in FRAMEWORKS_AND_TECHNIQUES.items():
        fw_code = marco_data["framework_code"]
        for tec_code, tec_data in marco_data["tecnicas"].items():
            result[tec_code] = {
                "nombre": tec_data["nombre"],
                "descripcion": tec_data["descripcion"],
                "marco": marco_name,
                "framework_code": fw_code,
                "codigo_interno": tec_code,
            }
    return result


def get_tecnica_to_framework_map():
    """Returns {codigo_interno: framework_name} for validation."""
    result = {}
    for marco_name, marco_data in FRAMEWORKS_AND_TECHNIQUES.items():
        for tec_code in marco_data["tecnicas"]:
            result[tec_code] = marco_name
    return result


def get_framework_to_tecnicas_map():
    """Returns {framework_name: [codigo_interno, ...]} for validation."""
    result = {}
    for marco_name, marco_data in FRAMEWORKS_AND_TECHNIQUES.items():
        result[marco_name] = list(marco_data["tecnicas"].keys())
    return result


# ─────────────────────────────────────────────────────────────
# 3. KEYWORD TO FRAMEWORK MAPPING (for AI recommendation)
# ─────────────────────────────────────────────────────────────

KEYWORD_TO_FRAMEWORKS = {
    # Dolor físico / musculoesquelético
    "dolor": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "dolor lumbar": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "dolor espalda": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "dolor cuello": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "contractura": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Vibracional / Energético Sutil"],
    "migraña": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "cefalea": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "articulación": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "artritis": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "fractura": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)"],
    "lesión": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)"],
    "postura": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "tensión muscular": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)"],
    "dolor crónico": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Psicosomático (Mente-Cuerpo-Emoción)"],

    # Digestivo / nutricional
    "digestión": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "estómago": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "intestino": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "colon": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "náusea": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "alimentación": ["Biomédico (Occidental)", "Ayurveda"],
    "peso": ["Biomédico (Occidental)", "Ayurveda"],
    "apetito": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "intolerancia": ["Biomédico (Occidental)", "Ayurveda"],
    "inflamación": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],

    # Respiratorio
    "respiración": ["Biomédico (Occidental)", "Ayurveda", "Vibracional / Energético Sutil"],
    "asma": ["Biomédico (Occidental)", "Ayurveda", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "alergia": ["Biomédico (Occidental)", "Ayurveda", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "tos": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],

    # Emocional / psicológico
    "ansiedad": ["Psicosomático (Mente-Cuerpo-Emoción)", "Ayurveda", "Vibracional / Energético Sutil"],
    "estrés": ["Psicosomático (Mente-Cuerpo-Emoción)", "Ayurveda", "Vibracional / Energético Sutil"],
    "depresión": ["Psicosomático (Mente-Cuerpo-Emoción)", "Biomédico (Occidental)", "Vibracional / Energético Sutil"],
    "insomnio": ["Psicosomático (Mente-Cuerpo-Emoción)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "miedo": ["Psicosomático (Mente-Cuerpo-Emoción)", "Vibracional / Energético Sutil", "Socio-familiar (Contexto y Sistemas)"],
    "tristeza": ["Psicosomático (Mente-Cuerpo-Emoción)", "Vibracional / Energético Sutil"],
    "angustia": ["Psicosomático (Mente-Cuerpo-Emoción)", "Vibracional / Energético Sutil", "Socio-familiar (Contexto y Sistemas)"],
    "ira": ["Psicosomático (Mente-Cuerpo-Emoción)", "Medicina Tradicional China (MTC)", "Socio-familiar (Contexto y Sistemas)"],
    "rabia": ["Psicosomático (Mente-Cuerpo-Emoción)", "Medicina Tradicional China (MTC)"],
    "frustración": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)"],
    "pánico": ["Psicosomático (Mente-Cuerpo-Emoción)", "Vibracional / Energético Sutil"],
    "trauma": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)"],
    "duelo": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)"],
    "pérdida": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)"],

    # Familiar / relacional
    "familia": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "pareja": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "hijos": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "padres": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "relación": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "conflicto": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "separación": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "divorcio": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "abandono": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "límites": ["Socio-familiar (Contexto y Sistemas)", "Psicosomático (Mente-Cuerpo-Emoción)"],

    # Energético / sutil
    "energía": ["Vibracional / Energético Sutil", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "cansancio": ["Biomédico (Occidental)", "Ayurveda", "Vibracional / Energético Sutil"],
    "fatiga": ["Biomédico (Occidental)", "Ayurveda", "Vibracional / Energético Sutil"],
    "agotamiento": ["Biomédico (Occidental)", "Ayurveda", "Vibracional / Energético Sutil", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "bloqueo": ["Vibracional / Energético Sutil", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "desequilibrio": ["Vibracional / Energético Sutil", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "chakra": ["Vibracional / Energético Sutil", "Ayurveda"],
    "aura": ["Vibracional / Energético Sutil"],

    # Piel / tejidos
    "piel": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "eczema": ["Biomédico (Occidental)", "Ayurveda", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "psoriasis": ["Biomédico (Occidental)", "Ayurveda", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "acné": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],

    # Cardiovascular
    "corazón": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "presión": ["Biomédico (Occidental)", "Ayurveda", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "hipertensión": ["Biomédico (Occidental)", "Ayurveda", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "circulación": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],

    # Hormonal / endocrino
    "hormona": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "tiroides": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "menopausia": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "ciclo": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "fertilidad": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],

    # Neurológico
    "neurológico": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Vibracional / Energético Sutil"],
    "mareo": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Ayurveda"],
    "vértigo": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Ayurveda"],
    "hormigueo": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)", "Ayurveda"],
    "entumecimiento": ["Biomédico (Occidental)", "Medicina Tradicional China (MTC)"],

    # General / sistémico
    "sistema inmune": ["Biomédico (Occidental)", "Ayurveda", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "inmunidad": ["Biomédico (Occidental)", "Ayurveda", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "infección": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "fiebre": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "sueño": ["Psicosomático (Mente-Cuerpo-Emoción)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "descanso": ["Psicosomático (Mente-Cuerpo-Emoción)", "Ayurveda", "Vibracional / Energético Sutil"],
    "concentración": ["Biomédico (Occidental)", "Ayurveda", "Psicosomático (Mente-Cuerpo-Emoción)"],
    "memoria": ["Biomédico (Occidental)", "Ayurveda", "Medicina Tradicional China (MTC)"],
    "sentido": ["Psicosomático (Mente-Cuerpo-Emoción)", "Vibracional / Energético Sutil", "Socio-familiar (Contexto y Sistemas)"],
    "propósito": ["Psicosomático (Mente-Cuerpo-Emoción)", "Vibracional / Energético Sutil", "Socio-familiar (Contexto y Sistemas)"],
    "existencia": ["Psicosomático (Mente-Cuerpo-Emoción)", "Vibracional / Energético Sutil"],
    "crisis": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)", "Vibracional / Energético Sutil"],
    "cambio": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)"],
    "transición": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)"],
    "identidad": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)"],
    "autoestima": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)"],
    "valoración": ["Psicosomático (Mente-Cuerpo-Emoción)", "Socio-familiar (Contexto y Sistemas)"],
    "desvalorización": ["Psicosomático (Mente-Cuerpo-Emoción)", "Vibracional / Energético Sutil"],
}
