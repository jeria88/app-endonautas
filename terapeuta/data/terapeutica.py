"""
Bloques de terapéutica de autoaplicación (Parte 6 de ambos manuales).

Indexados por PRINCIPIO de tratamiento, que se deriva de la fórmula MTC:
tonificar lo Deficiente, dispersar lo Excesivo, calentar lo Frío, enfriar lo
Calor, mover lo estancado, drenar la Humedad (Manual MTC 6.1).

Todo es autoadministrable sin agujas ni instrumentos: dieta, acupresión con los
dedos, respiración, movimiento suave y gestión emocional. La propuesta del paso 5
ensambla estos bloques según los ejes dominantes; la IA solo los redacta y
personaliza. PENDIENTE de validación por Franco.
"""

# Principios de tratamiento → bloque de autoaplicación
PRINCIPIOS = {
    "enfriar": {
        "titulo": "Clarificar el Calor (enfriar)",
        "cuando": "Predomina el Calor: sensación de calor, sed de agua fría, orina oscura, lengua roja con saburra amarilla.",
        "dieta": "Favorece alimentos frescos: pepino, apio, pera, sandía, menta, tofu, hoja verde. Evita picante, alcohol, frituras, cordero y café.",
        "acupresion": "LI-11 (Qu Chi, en el pliegue del codo por fuera) y LI-4 (He Gu, entre pulgar e índice): presión firme en círculos 1-2 min, 2-3×/día. Dispersan el Calor.",
        "estilo_vida": "Evita el sobreabrigo y el calor ambiental. Reposo. Baños tibios, no calientes.",
    },
    "calentar": {
        "titulo": "Tonificar y calentar el Yang",
        "cuando": "Predomina el Frío: mucho frío, extremidades frías, heces blandas, orina clara, todo mejora con el calor.",
        "dieta": "Favorece alimentos cálidos y cocidos: jengibre, canela, cebolla, caldos tibios, mijo. Evita helados, crudos en exceso y bebidas frías.",
        "acupresion": "ST-36 (Zu San Li, bajo la rótula) y KI-3 (Tai Xi, tras el maléolo interno). Calor local (bolsa térmica) sobre la zona baja del vientre y la zona lumbar.",
        "estilo_vida": "Abriga la zona lumbar y los pies. Movimiento suave que genere calor. Evita la exposición al Frío y la Humedad.",
    },
    "tonificar_qi": {
        "titulo": "Tonificar el Qi (nutrir la energía)",
        "cuando": "Predomina la Deficiencia de Qi: fatiga, voz débil, sudor espontáneo, pesadez tras comer.",
        "dieta": "Comidas tibias, cocidas y en horario fijo: arroz con jengibre, mijo, caldo de pollo, calabaza. No saltarse comidas ni abusar de crudos y fríos.",
        "acupresion": "ST-36 (Zu San Li) y SP-3/CV-12 (centro del abdomen): círculos suaves 1-2 min. Tonifican el Qi del Bazo y el Estómago.",
        "estilo_vida": "Descanso suficiente. No comer mientras se piensa o trabaja (la preocupación daña el Bazo). Movimiento suave, sin agotarse.",
    },
    "nutrir_yin": {
        "titulo": "Nutrir el Yin (humedecer y enfriar el vacío)",
        "cuando": "Deficiencia de Yin: calor por las tardes/noches, sudor nocturno, boca seca, lengua roja sin capa.",
        "dieta": "Alimentos que nutren el Yin: pera, tofu, sésamo, semillas, mijo, algas. Evita picante, alcohol, café y frituras.",
        "acupresion": "KI-3 (Tai Xi), KI-6 (Zhao Hai) y SP-6 (San Yin Jiao, sobre el maléolo interno): presión suave y sostenida.",
        "estilo_vida": "Sueño temprano y suficiente (el Yin se restaura de noche). Evita el exceso de trabajo y los estimulantes que consumen el Yin.",
    },
    "nutrir_sangre": {
        "titulo": "Nutrir la Sangre",
        "cuando": "Deficiencia de Sangre: palidez, piel seca, mareo con visión borrosa, uñas quebradizas.",
        "dieta": "Alimentos que tonifican la Sangre: espinaca, remolacha, granada, dátiles, huevo, legumbres. Evita el exceso de crudos.",
        "acupresion": "SP-6 (San Yin Jiao) y BL-17 (Ge Shu, entre los omóplatos): punto de la Sangre. Auto-masaje con aceite de sésamo sobre la piel seca.",
        "estilo_vida": "Sueño suficiente. Evita el desgaste sostenido y las pérdidas (revisa posible anemia con tu médico).",
    },
    "mover_qi": {
        "titulo": "Mover el Qi (deshacer el estancamiento)",
        "cuando": "Estancamiento de Qi: distensión que varía con el ánimo, suspiros, irritabilidad, dolor que se mueve.",
        "dieta": "Alimentos que mueven el Qi: cítricos, cebollino, pimienta suave, menta. Evita el exceso de grasa y lácteos.",
        "acupresion": "LR-3 (Tai Chong, dorso del pie entre 1° y 2° dedo) + LI-4 (He Gu): las '4 puertas', mueven Qi y Sangre. Círculos firmes 60s.",
        "estilo_vida": "Movimiento diario (caminar, Taiji, danza). Respiración lenta. Expresar y soltar la ira en vez de reprimirla.",
    },
    "mover_sangre": {
        "titulo": "Mover la Sangre (deshacer la estasis)",
        "cuando": "Estasis de Sangre: dolor fijo y punzante, peor de noche y en reposo, labios oscuros, várices.",
        "dieta": "Cúrcuma, jengibre, remolacha; Omega-3 (pescado azul, linaza). Calor suave local ayuda a mover.",
        "acupresion": "SP-10 (Xue Hai, sobre la rodilla interna) y SP-6. Auto-masaje ascendente de las extremidades. Movimiento suave diario.",
        "estilo_vida": "Evita la inactividad prolongada. Calor local suave sobre la zona (salvo si hay calor o sangrado).",
    },
    "drenar_humedad": {
        "titulo": "Drenar la Humedad / Mucosidad",
        "cuando": "Humedad/Tan: pesadez, hinchazón, saburra grasienta, lesiones que supuran, somnolencia.",
        "dieta": "Alimentos que drenan Humedad: judías, cebada, calabaza, rábano, jengibre. Evita dulces, lácteos, fritos y alcohol (generan Humedad).",
        "acupresion": "SP-9 (Yin Ling Quan, bajo la rodilla interna) y ST-36. Mantén las zonas afectadas secas y ventiladas.",
        "estilo_vida": "Ejercicio que haga sudar suavemente. Evita ambientes húmedos y las comidas pesadas por la noche.",
    },
    "dispersar_viento": {
        "titulo": "Dispersar el Viento",
        "cuando": "Viento: síntomas que cambian de lugar, aparición súbita, picor migratorio, sensibilidad a corrientes.",
        "dieta": "Según se combine con Calor o Frío (ver esos bloques). En Viento-Calor, enfría; en Viento-Frío, calienta con jengibre.",
        "acupresion": "GB-20 (Feng Chi, base del cráneo) y LI-4 (He Gu): dispersan el Viento. Protege la nuca de las corrientes.",
        "estilo_vida": "Evita las corrientes de aire y los cambios bruscos de temperatura. Cubre cuello y cabeza en clima ventoso.",
    },
}

# Mapa eje/condición dominante → principio(s) sugerido(s). El motor elige según
# la fórmula sintetizada (ver views._principios_desde_formula).
FASES_14_DIAS = [
    {"nombre": "Días 1-3 — Observar y ajustar", "objetivo": "Aplicar los cambios de dieta y una rutina de acupresión diaria; observar qué alivia y qué agrava (Upashaya)."},
    {"nombre": "Días 4-10 — Sostener", "objetivo": "Mantener dieta, acupresión y respiración/movimiento a diario. Anotar cambios en energía, sueño, digestión y síntoma principal."},
    {"nombre": "Días 11-14 — Reevaluar", "objetivo": "Volver a mirar la lengua y repetir la anamnesis. Comparar la fórmula. Si no hay mejoría o hay empeoramiento, derivar (Apéndice C)."},
]

RED_FLAGS_DERIVACION = (
    "Deriva de inmediato a atención médica si aparece: dolor torácico o dificultad "
    "para respirar, sangrado inusual, fiebre alta persistente (>3 días), pérdida de "
    "peso inexplicada, déficit neurológico (parálisis, confusión), o cualquier lesión "
    "que supura, se extiende con rapidez o compromete tu estado general."
)
