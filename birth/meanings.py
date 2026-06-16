# birth/meanings.py — Textos interpretativos en lenguaje simple para cada valor posible.
# Todos en segunda persona singular (tú), cálidos y directos.

# ── Carta Astral ──────────────────────────────────────────────────────────────

PLANET_MEANINGS = {
    'sun':     'Tu identidad central — la forma en que expresas tu esencia más auténtica y brillas en el mundo.',
    'moon':    'Tu mundo emocional interior — necesidades de seguridad, instintos y cómo te nutres y cuidas.',
    'mercury': 'Tu mente y comunicación — cómo piensas, aprendes, procesas ideas y te expresas con palabras.',
    'venus':   'Lo que valoras y deseas — tu estilo de amar, relacionarte, encontrar placer y crear belleza.',
    'mars':    'Tu energía y acción — la fuerza con que persigues lo que quieres y defiendes lo tuyo.',
    'jupiter': 'Tu área de expansión y abundancia — dónde creces con facilidad, aprendes y encuentras suerte.',
    'saturn':  'Tus lecciones de vida — dónde necesitas estructura, disciplina y madurar para crecer de verdad.',
    'uranus':  'Tu impulso de libertad y originalidad — dónde rompes esquemas y buscas lo diferente.',
    'neptune': 'Tu espiritualidad y mundo de los sueños — dónde disuelves límites y conectas con algo mayor.',
    'pluto':   'Tu poder de transformación profunda — dónde mueres y renaces a lo largo de la vida.',
}

SIGN_MEANINGS = {
    'Aries':       'Con impulso y valentía directa. Eres pionero natural que actúa antes de pensar.',
    'Tauro':       'Con paciencia y sensorialidad. Buscas estabilidad, placer y construyes con calma.',
    'Géminis':     'Con curiosidad y adaptabilidad. Tu mente es rápida y versátil, necesita variedad constante.',
    'Cáncer':      'Con sensibilidad e intuición profunda. Te mueves desde el corazón y el cuidado es tu lenguaje.',
    'Leo':         'Con creatividad y generosidad natural. Brillas cuando te expresas con autenticidad y calidez.',
    'Virgo':       'Con análisis y precisión. Encuentras sentido en mejorar, servir y atender al detalle.',
    'Libra':       'Con armonía y búsqueda de equilibrio. Valoras la justicia, la belleza y la conexión genuina.',
    'Escorpio':    'Con intensidad y profundidad. No te quedas en la superficie — vas al fondo de todo.',
    'Sagitario':   'Con expansión y búsqueda de sentido. Necesitas libertad, aventura y un horizonte amplio.',
    'Capricornio': 'Con ambición y disciplina. Construyes paso a paso con visión de largo plazo y determinación.',
    'Acuario':     'Con originalidad e independencia. Piensas diferente y aportas perspectivas que nadie más tiene.',
    'Piscis':      'Con empatía y espiritualidad. Disuelves fronteras y conectas con lo que no se ve ni se toca.',
}

ASC_MEANINGS = {
    'Aries':       'Te presentas al mundo como alguien directo, enérgico y decidido. La gente te percibe como una fuerza en movimiento. Tu primera impresión es de confianza y valentía.',
    'Tauro':       'Proyectas calma, solidez y confiabilidad. La gente siente que puede apoyarse en ti. Tu presencia tiene un efecto tranquilizador natural en el entorno.',
    'Géminis':     'Te presentas como alguien curioso, comunicativo y lleno de ideas. La gente nota tu agilidad mental. Tu presencia es ligera, adaptable y estimulante.',
    'Cáncer':      'Proyectas calidez y cuidado palpable. La gente siente que puede confiar en ti desde el primer momento. Tu primera impresión es de hogar y contención.',
    'Leo':         'Te presentas con presencia magnética y calidez natural. La gente nota cuando entras a un lugar. Tu primer impacto es generoso y carismático.',
    'Virgo':       'Proyectas orden, atención y competencia tranquila. La gente te percibe como alguien detallista y confiable. Tu presencia inspira que las cosas están bien hechas.',
    'Libra':       'Te presentas con gracia y elegancia natural. La gente te percibe como alguien equilibrado y agradable. Tu presencia suaviza el ambiente donde estás.',
    'Escorpio':    'Proyectas intensidad y misterio. La gente siente que hay más de lo que muestras. Tu mirada llega antes que tus palabras.',
    'Sagitario':   'Te presentas con entusiasmo y una energía expansiva. La gente te percibe como alguien optimista y libre. Tu presencia inspira ganas de explorar.',
    'Capricornio': 'Proyectas madurez y competencia. La gente te percibe como alguien que sabe lo que hace. Tu primera impresión es de autoridad tranquila y seria.',
    'Acuario':     'Te presentas como alguien único e impredecible. La gente nota que piensas diferente. Tu presencia es estimulante y difícil de encasillar.',
    'Piscis':      'Proyectas sensibilidad y apertura. La gente siente que eres receptivo y empático. Tu primer impacto es suave y difícil de definir con precisión.',
}

MC_MEANINGS = {
    'Aries':       'Eres reconocido por tu valentía e iniciativa. Tu vocación tiene energía pionera — lideras hacia lo nuevo.',
    'Tauro':       'Eres recordado por lo que construyes con constancia. Tu vocación tiene base material, tangible y duradera.',
    'Géminis':     'Eres reconocido por tu comunicación y capacidad de conectar ideas. Tu vocación involucra el lenguaje y el intercambio.',
    'Cáncer':      'Eres recordado por tu capacidad de cuidar y crear pertenencia. Tu vocación tiene un corazón nutrido y protector.',
    'Leo':         'Eres reconocido por tu creatividad y autenticidad. Tu vocación involucra liderar desde el corazón y brillar.',
    'Virgo':       'Eres recordado por tu excelencia y servicio. Tu vocación involucra perfeccionar, sanar y mejorar con método.',
    'Libra':       'Eres reconocido por tu diplomacia y sentido de justicia. Tu vocación involucra crear armonía entre personas.',
    'Escorpio':    'Eres recordado por tu profundidad y poder de transformación. Tu vocación toca lo que otros evitan mirar.',
    'Sagitario':   'Eres reconocido por tu visión y sabiduría. Tu vocación involucra enseñar, explorar o expandir horizontes.',
    'Capricornio': 'Eres recordado por tus logros y lo que construyes. Tu vocación tiene una dimensión de legado y estructura.',
    'Acuario':     'Eres reconocido por tu originalidad y visión de futuro. Tu vocación involucra romper moldes y aportar al colectivo.',
    'Piscis':      'Eres recordado por tu compasión y creatividad espiritual. Tu vocación tiene una dimensión de sanación o trascendencia.',
}

# ── Human Design ──────────────────────────────────────────────────────────────

HD_TYPE_MEANINGS = {
    'Generador': 'Eres el motor del mundo — tu energía sacral es la fuerza más sostenida del planeta. Funciona de verdad cuando la diriges hacia lo que te genera un "sí" visceral. Esperar a responder (en vez de iniciar desde la mente) es la clave de tu vida.',
    'Generador Manifestante': 'Tienes energía sacral Y capacidad de iniciar. Eres potente y rápido, pero informar antes de actuar reduce la resistencia. Tu ciclo natural: sentir → responder → informar → hacer.',
    'Manifestador': 'Tienes el impulso de poner cosas en movimiento sin necesitar permiso. Tu energía inicia y cataliza. El reto es informar a quienes te rodean antes de actuar — eso reduce el aislamiento y la resistencia del entorno.',
    'Proyector': 'Naciste para guiar, reconocer y optimizar — no para trabajar sin parar. Tu energía es de insight y dirección, no de producción constante. Esperar la invitación antes de ofrecer tu visión garantiza que sea recibida y valorada.',
    'Reflector': 'Eres el espejo de tu comunidad: reflejas su salud y estado real. Tu apertura total a las energías de otros es un don, no una debilidad. Las decisiones importantes necesitan tiempo — un ciclo lunar completo (29 días) es tu ritmo natural.',
}

HD_PROFILE_MEANINGS = {
    '1/1': 'Investigador profundo que necesita una base sólida de conocimiento para moverse con seguridad. Mientras más estudias, más confianza sientes.',
    '1/2': 'Investigas profundo y de repente eres llamado a compartir lo que sabes, aunque no te lo hayas propuesto. Alternas entre estudiar y necesitar soledad para integrar.',
    '1/3': 'Aprendes todo lo que puedes y lo pruebas en la vida real hasta que algo deja de funcionar. Tus "fracasos" son tu mayor fuente de maestría — no son tropiezos, son datos.',
    '1/4': 'Tu conocimiento se comparte a través de relaciones de confianza. Tu base de información es el capital que te permite influir en tu círculo cercano.',
    '2/1': 'Tienes dones naturales que no siempre reconoces en ti mismo. Necesitas soledad para recargarte y eres llamado por otros sin haberlo buscado activamente.',
    '2/2': 'Dos ermitaños: necesitas mucha soledad para que tus dones naturales emerjan. Nadie te enseña — floreces solo cuando el entorno correcto lo activa.',
    '2/3': 'Naturaleza hermitaña con proceso experimental. Eres llamado a salir de tu mundo para probar cosas. Aprendes principalmente por ensayo y error.',
    '2/4': 'Dones naturales que se comparten a través de relaciones de confianza. Eres convocado a compartir lo que tienes sin haberlo buscado activamente.',
    '3/1': 'Aprendes por experimentación y lo que no funciona. Tu base investigativa más tu experiencia pragmática son tu mayor autoridad.',
    '3/2': 'Procesas la vida por ensayo-error y necesitas soledad para integrar. Tus "fracasos" tempranos son semillas de sabiduría profunda.',
    '3/3': 'Triple mártir: aprendes completamente por experiencia real. Tus múltiples tropiezos son en realidad una maestría profunda en lo que no funciona.',
    '3/4': 'Aprendes por experiencia y lo compartes con tu red cercana. Las relaciones son fundamentales en tu proceso de aprendizaje y propósito.',
    '4/1': 'Yuxtaposición: estás en un camino fijo con su propia lógica. Influyes en tu red desde un conocimiento bien fundamentado y relaciones estables.',
    '4/2': 'Buscas seguridad en relaciones estables, con dones naturales que emergen solos. Tu red social es el canal de tu propósito.',
    '4/3': 'Aprendes por experiencia y lo compartes con tu red. Las crisis son oportunidades de renovar vínculos y reorientar.',
    '4/4': 'Doble oportunista: tu propósito se mueve completamente a través de personas y redes. Las relaciones son tu único canal real.',
    '5/1': 'Eres percibido como alguien que tiene algo especial o que puede resolver lo que otros no pueden. Necesitas una base sólida para que las proyecciones no te abrumen.',
    '5/2': 'Eres percibido como solución o salvador. Necesitas soledad para recargarte y una base firme para sostenerte ante lo que proyectan en ti.',
    '5/3': 'Eres percibido como referente. Aprendes por ensayo-error en privado y emerges con maestría práctica que inspira a otros.',
    '5/4': 'Eres percibido como quien tiene algo valioso. Las proyecciones te buscan — necesitas base sólida y relaciones confiables para sostenerte.',
    '6/1': 'Dos fases de vida: primero prueba y error intenso (hasta los ~30), luego observación y reflexión desde el tejado. En la madurez, eres un modelo de rol genuino.',
    '6/2': 'Modelo de rol con dones naturales: una primera fase experimental y luego emerger como referente desde la autenticidad y los dones que te son propios.',
    '6/3': 'Modelo de rol que aprendió por tropiezos. Tus experiencias tempranas difíciles son la base de tu autoridad real y tu sabiduría.',
    '6/4': 'Modelo de rol que actúa a través de su red. Tu autoridad viene de la experiencia vivida y se expresa a través de relaciones de confianza.',
}

HD_AUTHORITY_MEANINGS = {
    'Emocional — Plexo Solar': 'No hay claridad real en el momento de la emoción. Espera a que la ola emocional suba y baje — la respuesta correcta se mantiene clara con el tiempo, no en el pico.',
    'Sacral':                  'Tu cuerpo sabe antes que tu mente. Observa la respuesta visceral — ese "uh-huh" (sí) o "un-un" (no) que surge instantáneamente antes de que la mente intervenga.',
    'Esplénico — Bazo':        'Tu claridad es instantánea e intuitiva — una voz suave que aparece una sola vez y no repite. Aprende a reconocerla antes de que la mente la tape con razones.',
    'Ego — Corazón':           'Lo que tu corazón quiere y puede sostener es tu brújula real. Habla en voz alta sobre lo que decides — escucharte a ti mismo te aclara más que pensar en silencio.',
    'Identidad — G':           'Tu claridad surge en conversación y en el lugar correcto. No decides solo — el entorno y las personas de confianza te ayudan a saber qué sientes.',
    'Lunar — 29 días':         'Cada decisión importante necesita vivirse durante un ciclo lunar. Observa cómo te sientes con ella en distintos momentos y contextos a lo largo de 29 días.',
    'Mental — Externo':        'Tu autoridad surge al hablar en voz alta con personas de confianza — no para que te aconsejen, sino para escucharte a ti mismo. El proceso es la conversación.',
}

HD_DEFINITION_MEANINGS = {
    'Indefinido':            'No tienes centros definidos — eres puro espacio de apertura y recepción. Absorbes y amplificas las energías de tu entorno. Tu mayor don es tu capacidad de reflexión.',
    'Definición Simple':     'Tu energía fluye de forma consistente y predecible — eres lo mismo en la mayoría de contextos. No necesitas de otros para sentirte completo energéticamente.',
    'Definición Partida':    'Tienes dos circuitos de energía separados. Ciertas personas "cierran el puente" entre ambos, activando una sensación de wholeness que no siempre tienes solo.',
    'Definición Partida Triple': 'Tres circuitos separados — eres complejo y puedes parecer diferente en distintos contextos. Distintas personas activan distintas partes de ti.',
    'Definición Cuádruple':  'Cuatro circuitos separados — extremadamente complejo y adaptable. Casi siempre necesitas de otros para completar y activar tu energía.',
}

HD_CENTER_MEANINGS = {
    'Cabeza':      'Centro de inspiración e ideas. Definido: generas preguntas e inspiración de forma consistente y confiable.',
    'Ajna':        'Centro de procesamiento mental. Definido: tienes una forma fija y reconocible de procesar y analizar información.',
    'Garganta':    'Centro de manifestación y comunicación. Definido: tienes voz y presencia consistentes — expresas y haces que las cosas ocurran.',
    'Identidad':   'Centro del yo y la dirección de vida. Definido: sabes quién eres y hacia dónde vas, aunque el contexto cambie.',
    'Corazón':     'Centro de la voluntad y el ego. Definido: tienes fuerza de voluntad consistente y capacidad de comprometerte y cumplir.',
    'Plexo Solar': 'Centro emocional. Definido: tienes un ciclo emocional propio que es tu autoridad. La claridad llega con tiempo, no en el pico.',
    'Sacral':      'Centro de la fuerza vital. Definido: tienes energía sostenida para el trabajo y una respuesta gut instintiva que guía tus decisiones.',
    'Bazo':        'Centro de intuición esplénica. Definido: tienes intuición en tiempo real, un "saber" instantáneo que no se repite y no necesita justificarse.',
    'Raíz':        'Centro de presión adrenal. Definido: tienes un ritmo consistente para manejar la presión y la urgencia — no te desestabiliza fácilmente.',
}

# ── Saju / BaZi ──────────────────────────────────────────────────────────────

SAJU_PILLAR_MEANINGS = {
    'Año':  'Tu energía ancestral y social. Muestra tu relación con el mundo exterior, la familia de origen y el contexto cultural en que creciste.',
    'Mes':  'Tu pilar vocacional. Refleja tus dones naturales en el trabajo, tu estilo profesional y el camino del propósito.',
    'Día':  'Tu esencia personal — el yo más íntimo y auténtico. Es el pilar más importante para entenderte a ti mismo.',
    'Hora': 'Tu yo oculto: lo que pocas personas ven pero es profundamente tuyo. También refleja tu relación con hijos y el legado que dejas.',
}

SAJU_ELEMENT_MEANINGS = {
    'Madera': 'Crecimiento, expansión y visión. Como un árbol, buscas elevarte con raíces profundas. Energía creativa y orientada al futuro.',
    'Fuego':  'Pasión, transformación y presencia radiante. Iluminas los espacios donde estás y tienes capacidad natural de inspirar a otros.',
    'Tierra': 'Estabilidad, nutrición y centro. Eres el suelo fértil donde todo puede crecer — confiable, práctico y contenedor.',
    'Metal':  'Precisión, claridad y refinamiento. Tienes capacidad de cortar lo esencial, encontrar la verdad y perfeccionar lo que tocas.',
    'Agua':   'Fluidez, profundidad e introspección. Como el agua, encuentras el camino aunque no sea recto. Gran capacidad de adaptación y sabiduría interior.',
}

SAJU_DAYMASTER_MEANINGS = {
    'Madera Yang': 'Eres el árbol robusto: directo, ambicioso y con visión clara de crecimiento. Fuerte pero puedes ser rígido cuando se exige demasiado.',
    'Madera Yin':  'Eres la enredadera flexible: adaptable, persistente y capaz de encontrar el camino aunque el terreno sea difícil.',
    'Fuego Yang':  'Eres el sol: radiante, expansivo y generador de energía para todos a tu alrededor. Tu presencia es poderosa e inmediata.',
    'Fuego Yin':   'Eres la llama de una vela: cálido, íntimo y constante. Iluminas de cerca con una intensidad sostenida y profunda.',
    'Tierra Yang': 'Eres la montaña: sólido, confiable y lleno de recursos. Provees estabilidad y apoyo para quienes te rodean.',
    'Tierra Yin':  'Eres el suelo fértil: receptivo y generador de crecimiento en todo lo que tocas. Nutre sin pedir nada a cambio.',
    'Metal Yang':  'Eres el hacha: directo, cortante y capaz de hacer la diferencia con precisión. Tienes autoridad natural y claridad de propósito.',
    'Metal Yin':   'Eres la joya pulida: refinado, detallista y capaz de brillar con la preparación adecuada. La excelencia es tu estándar.',
    'Agua Yang':   'Eres el océano: profundo, poderoso y misterioso. Tu fuerza es inmensa aunque no siempre sea visible para los demás.',
    'Agua Yin':    'Eres el arroyo tranquilo: gentil, adaptable y con una sabiduría que fluye sin esfuerzo ni urgencia.',
}

SAJU_ANIMAL_MEANINGS = {
    'Rata':       'Inteligente, adaptable y con instinto para las oportunidades. Sociable y con habilidad natural para acumular recursos.',
    'Buey':       'Trabajador, perseverante y confiable. Lento pero constante — siempre llega a la meta sin importar los obstáculos.',
    'Tigre':      'Valiente, carismático y con presencia magnética. Lidera por naturaleza y no acepta fácilmente que le digan cómo hacerlo.',
    'Conejo':     'Sensible, diplomático y con gusto artístico refinado. Crea armonía en el entorno y tiene instinto natural para la belleza.',
    'Dragón':     'Poderoso, visionario y con una energía que inspira a quienes le rodean. Nació para destacar y dejar huella.',
    'Serpiente':  'Intuitivo, misterioso y profundamente sabio. Piensa antes de hablar y guarda más de lo que muestra.',
    'Caballo':    'Libre, enérgico y en movimiento constante. Necesita autonomía y aventura para dar lo mejor de sí.',
    'Cabra':      'Creativo, empático y con sensibilidad refinada. Necesita apoyo emocional y armonía para florecer.',
    'Mono':       'Ingenioso, versátil y con humor afilado. Aprende rápido y tiene capacidad de hacer casi cualquier cosa bien.',
    'Gallo':      'Detallista, puntual y con altos estándares propios. Trabaja duro y le importa cómo es percibido.',
    'Perro':      'Leal, justo y con un fuerte sentido ético. Protege a los suyos con determinación y no tolera la injusticia.',
    'Cerdo':      'Generoso, honesto y apasionado. Confía en los demás con facilidad y disfruta los placeres simples de la vida.',
}
