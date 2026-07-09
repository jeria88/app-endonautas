"""Diagnosticos de marcos no-MTC (PSI/SOC/VIB/BIO/AYU).
Se puntuan por pesos directos signo->dx desde anamnesis.py (campo "dx" de cada opcion).
Los diagnosticos MTC migraron a patrones_mtc.py como firmas de ejes.
"""

DIAGNOSIS_OTROS = [{'id': 'D02',
  'titulo': 'Desequilibrio Vata-Pitta',
  'descripcion': 'Alteración de los doshas Vata (aire/movimiento) y Pitta (fuego/metabolismo) que genera ansiedad, '
                 'sequedad, ardor y desregulación digestiva.',
  'marco_asociado': 'Ayurveda',
  'tecnica_asociada': 'AYU-DIE',
  'sintomas': ['ansiedad',
               'ardor estomacal',
               'sequedad piel',
               'insomnio',
               'gases',
               'alternancia diarrea/estreñimiento'],
  'etiologia': 'El desequilibrio combinado Vata-Pitta surge cuando a la movilidad e irregularidad de Vata (aire/éter) '
               'se suma la inflamación y reactividad de Pitta (fuego/agua). Causas más frecuentes: viajes frecuentes o '
               'cambios de rutina (agrava Vata), dieta con exceso de picante/ácido/salado (agrava Pitta), exposición '
               'solar excesiva, trabajo bajo presión con plazos ajustados, consumo regular de café y alcohol.',
  'mecanismo': 'Vata perturbado genera sequedad en todos los canales: intestino seco (constipación) que alterna con '
               'evacuación rápida. Pitta perturbado produce fuego en el tracto digestivo (ardor, acidez) y en la '
               'sangre (inflamación cutánea). La combinación genera un estado de nerviosismo ardiente: la mente activa '
               "y ansiosa de Vata más la reactividad irritable de Pitta (ref. Lad 'Textbook of Ayurveda Vol.1', cap. "
               '4).',
  'patron_diagnostico': 'Evaluación de Prakruti/Vikruti (constitución natural vs. estado actual). Signos de Vata: '
                        'lengua con grietas o revestimiento marrón seco, pulso fino, rápido, irregular. Signos de '
                        'Pitta: capa amarilla en lengua, pulso rápido y cortante, ojos rojizos. Clínico: ansiedad con '
                        'bordes de enojo, ardor gástrico, diarrea o alternancia, sed excesiva, piel con brotes.',
  'protocolo_indicado': "Protocolo de dietoterapia para Vata-Pitta aggravado (ref. Lad 'Textbook of Ayurveda Vol.1', "
                        "cap. 8; Pole 'Ayurvedic Medicine'). Principio: primero calmar Vata (rutina, alimentos tibios, "
                        'oleosos), luego enfriar Pitta (evitar exceso de picante y acidez). Alimentos recomendados: '
                        'arroz basmati con ghee, lentejas rojas (masoor dal), leche tibia con cardamomo, manzana '
                        'cocida con canela. Evitar: café, alcohol, alimentos muy picantes o ácidos (tomate, vinagre, '
                        'cítricos en exceso), crudos en exceso. Hierbas: Ashwagandha (Withania somnifera) 1-2g en '
                        'polvo con leche tibia al acostarse (calmante para Vata-Pitta); Shatavari (Asparagus '
                        'racemosus) 1g con ghee para Pitta y membrana mucosa; Triphala 1 cucharadita antes de dormir '
                        '(regulador digestivo tridóshico). Rituales: comer en horarios fijos, sin pantallas, en '
                        'ambiente tranquilo; no comer cuando hay enojo (agrava Pitta). Abhyanga (automasaje) con '
                        'aceite de sésamo (Vata) o coco (Pitta) 3 veces por semana antes del baño.',
  'contraindicaciones': 'No prescribir Ashwagandha si hay Pitta muy elevado con fiebre o inflamación activa (la hierba '
                        'es levemente calórica). No prescribir Triphala si hay diarrea activa. Ajustar las '
                        'proporciones de la dieta según cuál dosha predomina en el momento de la consulta.',
  'integracion': 'BIO-NUT: el ardor gástrico y la intolerancia alimentaria pueden evaluarse también desde FODMAP y '
                 'SIBO — los paradigmas son complementarios. PSI-PNI: el estrés que agrava ambos doshas es el mismo '
                 'cortisol que desregula el eje HPA — la gestión del estrés es transversal. BIO-FIS: el yoga como '
                 'práctica física tiene evidencia para reducir el cortisol y mejorar la HRV, complementando el '
                 'protocolo ayurvédico.'},
 {'id': 'D03',
  'titulo': 'Síndrome de Dolor Miofascial Lumbar',
  'descripcion': 'Presencia de puntos gatillo activos en la musculatura lumbar y glútea que generan dolor referido, '
                 'rigidez y limitación funcional. Es una de las causas más frecuentes de dolor lumbar crónico y '
                 'responde mal a los antiinflamatorios cuando no se trata la causa miofascial directamente.',
  'marco_asociado': 'Biomédico (Occidental)',
  'tecnica_asociada': 'BIO-FIS',
  'sintomas': ['puntos gatillo',
               'rigidez matinal',
               'dolor referido pierna',
               'limitación flexión',
               'dolor al estar sentado'],
  'etiologia': 'Sobreuso muscular, microtraumatismos repetitivos y postura inadecuada sostenida activan los puntos '
               'gatillo. Los factores perpetuantes incluyen deficiencias de vitamina D, magnesio y B12, hipotiroidismo '
               'subclínico, estrés crónico (el cortisol facilita la hipertonicidad muscular) y sueño no reparador. La '
               'isquemia focal en la placa motora es el mecanismo de inicio.',
  'mecanismo': 'Los puntos gatillo miofasciales son zonas de contracción sostenida en la placa motora que generan '
               'isquemia local. Esa isquemia sensibiliza los nociceptores locales y produce dolor referido según los '
               'mapas de Travell y Simons (dolor que se irradia a glúteo, cara posterior del muslo o incluso pie, sin '
               'que haya lesión nerviosa real). Con la cronicidad se produce sensibilización central: el umbral de '
               'dolor baja y el territorio de dolor se expande.',
  'patron_diagnostico': 'Evaluación postural buscando el patrón inferior cruzado de Janda (flexores de cadera tensos, '
                        'glúteos inhibidos, hiperlordosis lumbar). Palpación de bandas tensas con punto gatillo: el '
                        'punto es hipersensible, al presionarlo reproduce el dolor referido que describe el paciente. '
                        'Tests ortopédicos (Lasègue, Faber, test de Thomas) para descartar origen articular o '
                        'radicular. El diagnóstico diferencial principal es hernia discal con compresión radicular.',
  'protocolo_indicado': 'Liberación de puntos gatillo: presión isquémica directa (pulgar o codo) sobre el punto '
                        'gatillo durante 60-90 segundos hasta sentir que la tensión cede, 1-2 veces al día; dry '
                        'needling aplicado por fisioterapeuta certificado; spray & stretch (técnica de Travell: '
                        'aplicar cloruro de etilo en spray sobre la banda muscular tensa mientras se estira '
                        'pasivamente el músculo). Ejercicio terapéutico de estabilización lumbar — Fase 1: Bird-Dog: '
                        'en cuadrupedia (manos y rodillas), espalda neutral, inhala y al exhalar extiende '
                        'simultáneamente el brazo derecho hacia adelante y la pierna izquierda hacia atrás, mantén 3 '
                        'segundos, vuelve al centro. Alterna lados. 3 series de 8 repeticiones cada lado, en días '
                        'alternos. Dead Bug: tumbado boca arriba, rodillas en 90°, brazos al techo. Inhala. Al '
                        'exhalar, baja simultáneamente el brazo derecho hacia atrás y la pierna izquierda hacia el '
                        'suelo (sin llegar a tocar), mantén la zona lumbar pegada al suelo. Vuelve. Alterna. 3 series '
                        'de 6 repeticiones. Plancha frontal: apoyado en antebrazos y puntillas, cuerpo recto, mantener '
                        '20-30 segundos. 3 series. Corrección ergonómica: pantalla al nivel de los ojos (colocar '
                        'soporte si está más baja); respaldo de silla en contacto con la curva lumbar; pies planos en '
                        'el suelo o en reposapiés; cada 45 minutos, pausa activa de 5 minutos: levantarse, 5 '
                        'rotaciones de hombros hacia atrás, 5 círculos de cadera, 10 pasos caminando. Suplementación: '
                        'magnesio glicinato 300-400mg/día con la cena (el magnesio relaja la placa motora y reduce la '
                        'hipertonicidad muscular).',
  'contraindicaciones': 'No aplicar presión directa ni dry needling sobre zonas con compromiso vascular o nervioso. No '
                        'prescribir ejercicios de alta carga en fase aguda (primeras 72h). No ignorar señales de '
                        'alarma: dolor con fiebre, pérdida de control de esfínteres o debilidad progresiva requieren '
                        'derivación médica urgente.',
  'integracion': 'MTC: correlaciona con estancamiento de Sangre en los canales de vejiga y riñón. PSI-SOM: el '
                 'componente somático del trauma almacenado es frecuente en dolor lumbar crónico resistente al '
                 'tratamiento manual. PSI-PNI: el cortisol elevado por estrés crónico actúa como factor perpetuante; '
                 'sin gestión del estrés la recaída es casi segura.'},
 {'id': 'D04',
  'titulo': 'Conflicto de Separación',
  'descripcion': 'Conflicto emocional profundo relacionado con la pérdida de conexión significativa (pareja, familiar, '
                 'lugar) que se manifiesta en espalda alta y opresión torácica.',
  'marco_asociado': 'Socio-familiar (Contexto y Sistemas)',
  'tecnica_asociada': 'SOC-CON',
  'sintomas': ['dolor espalda alta',
               'opresión torácica',
               'sensación de vacío',
               'dificultad para soltar',
               'apego ansioso'],
  'etiologia': 'El conflicto de separación emerge cuando se pierde o amenaza un vínculo de pertenencia primario: '
               'ruptura de pareja, alejamiento de un hijo, pérdida de un hogar, separación de la tierra natal. Según '
               "Hellinger ('Love's Hidden Symmetry'), el ser humano tiene un impulso hacia el sistema familiar "
               '(Zugehörigkeit) que cuando se rompe genera un sufrimiento que busca restablecerse incluso a través del '
               'síntoma.',
  'mecanismo': 'En el marco de Constelaciones Familiares, los síntomas físicos en la espalda alta y el corazón '
               "corresponden al proceso de 'soltar' lo que se perdió. El diafragma y los músculos intercostales "
               'almacenan la tensión de la emoción no llorada. El síntoma protege al sistema: mientras el sufrimiento '
               'de la separación no sea reconocido y honrado, el cuerpo lo porta.',
  'patron_diagnostico': 'Historia relacional: explorar pérdidas de figuras de apego significativas, separaciones '
                        'traumáticas, exilios voluntarios o forzados. Síntomas corporales: opresión torácica sin causa '
                        'cardiológica, nudo en la garganta, dolor entre escápulas, dificultad para respirar profundo. '
                        "Pregunta diagnóstica clave de Hellinger: '¿A quién extrañas?' y '¿Qué parte de ti se fue con "
                        "esa persona o lugar?'",
  'protocolo_indicado': "Protocolo de Constelaciones Familiares para Conflicto de Separación (ref. Hellinger 'Love's "
                        "Hidden Symmetry', cap. 3; Franke 'My Way'). Fase 1 — Reconocimiento: facilitar (sesión "
                        'individual o grupal) que el consultante nombre explícitamente lo que se perdió y lo que '
                        'representaba. La constelación da un lugar al separado. Fase 2 — Movimiento de alma: en la '
                        'constelación, el movimiento típico es que el representante del consultante pueda mirar a '
                        "quien se separó, nombrar lo que fue, y hacer el gesto de soltar: 'Yo te recuerdo y te honro, "
                        "y me doy permiso de seguir mi camino'. Fase 3 — Integración: después de la sesión, journaling "
                        "con la pregunta '¿Qué de esa persona o lugar quiero integrar en quien soy ahora?' Rituales de "
                        'cierre: escribir una carta que no se envía, crear un altar de transición. Complemento: 3-5 '
                        'sesiones de duelo con enfoque humanista o gestáltico para acompañar el proceso emocional.',
  'contraindicaciones': 'Las Constelaciones Familiares no están indicadas en crisis psiquiátricas agudas (episodios '
                        "psicóticos, disociación grave activa). No forzar el proceso de 'soltar': cada sistema tiene "
                        'su propio tiempo. No trabajar la separación sin haber validado primero el dolor de la '
                        'pérdida.',
  'integracion': 'PSI-SOM: el trabajo corporal de Somatic Experiencing puede liberar la tensión torácica almacenada '
                 'antes o después de la constelación, facilitando el proceso. VIB-REI: el Reiki sobre el centro '
                 'cardíaco puede acompañar el proceso de apertura emocional. BIO-NUT: si el conflicto ha generado '
                 'pérdida del apetito o cambios en la alimentación, una evaluación nutricional es pertinente.'},
 {'id': 'D05',
  'titulo': 'Patrón de Resonancia de Desvalorización',
  'descripcion': 'Patrón energético limitante de baja autoestima y sensación de no merecer, que se manifiesta como '
                 'contracturas crónicas y apatía.',
  'marco_asociado': 'Vibracional / Energético Sutil',
  'tecnica_asociada': 'VIB-RES',
  'sintomas': ['apatía',
               'contracturas crónicas',
               'sensación de no merecer',
               'postura encorvada',
               'falta de motivación'],
  'etiologia': 'El patrón de desvalorización se instala cuando en etapas tempranas del desarrollo el entorno devolvió '
               "mensajes consistentes de 'no eres suficiente'. Estos mensajes quedan codificados en los neuropéptidos "
               "(Pert, 'Molecules of Emotion') y en patrones de tensión muscular y postura que se perpetúan "
               "automáticamente. La resonancia con la frecuencia de 'no merecer' se activa ante situaciones que "
               'recuerdan a la herida original.',
  'mecanismo': "Según la teoría del Resonance Repatterning (Schiff, 'The Resonance Repatterning Primer'), los patrones "
               'limitantes son frecuencias de resonancia que el sistema neuromuscular reproduce de forma automática. '
               "El cuerpo 'siente familiar' la frecuencia de la desvalorización porque fue el estado más frecuente en "
               'el pasado. La kinesiología aplicada permite identificar cuál frecuencia está en coherencia con el '
               'sistema y cuáles en anticoherencia.',
  'patron_diagnostico': 'Evaluación de resonancia mediante test muscular (kinesiología aplicada): qué afirmaciones de '
                        'valor propio generan debilitamiento muscular. Observación postural: hombros caídos hacia '
                        'adelante, cabeza adelantada, tendencia a hacerse pequeño. Historia: identificar el primer '
                        "momento en que se sintió 'menos que' o 'no suficiente'. Preguntas diagnósticas: '¿Con qué "
                        "frecuencia te escuchas diciéndote que no mereces?' y '¿Hay alguien en tu familia que haya "
                        "tenido la misma dificultad?'",
  'protocolo_indicado': "Protocolo de Resonance Repatterning para Desvalorización (ref. Schiff 'The Resonance "
                        "Repatterning Primer'; Beaulieu 'Music and Sound in the Healing Arts'). Fase 1 — "
                        'Identificación: el terapeuta guía al consultante a enunciar el patrón central en voz alta '
                        "('No merezco estar bien') mientras aplica test muscular para confirmar la resonancia. Fase 2 "
                        '— Aclaramiento: uso de modalidades de cambio de frecuencia. Opciones: respiración coherente '
                        '(5s inspiración / 5s espiración, 5-10 min) para activar el parasimpático; movimiento de '
                        'acceso ocular mientras se sostiene la frase opuesta; acupresión en PC-6 (Neiguan) + CV-17 '
                        '(Shanzhong) mientras se enuncia la frase positiva. Fase 3 — Reprogramación: el terapeuta '
                        'introduce afirmaciones de valor en el momento de mayor apertura fisiológica (post-respiración '
                        "coherente): 'Merezco estar bien. Mi bienestar importa.' Tarea para casa: 3 min de respiración "
                        'coherente antes de dormirse + afirmación en primera persona. Frecuencia: sesiones '
                        'quincenales; el trabajo se hace en capas.',
  'contraindicaciones': 'No aplicar en crisis emocional aguda: la identificación del patrón puede intensificar '
                        'temporalmente el sufrimiento. El test muscular requiere profesional certificado en '
                        'kinesiología aplicada: la autoaplicación genera resultados poco fiables.',
  'integracion': 'PSI-BIO: la desvalorización como patrón vibracional tiene correlato directo en el conflicto '
                 'biológico de desvalorización (D09), que se manifiesta en articulaciones y huesos. SOC-GEN: la raíz '
                 'del patrón suele ser transgeneracional; el genograma puede identificar a qué ancestro se está siendo '
                 'leal. BIO-FIS: la postura encorvada asociada al patrón responde a trabajo de reequilibrio muscular '
                 '(fisioterapia posturalista).'},
 {'id': 'D07',
  'titulo': 'Síndrome de Intestino Irritable (SII)',
  'descripcion': 'Trastorno funcional del eje intestino-cerebro caracterizado por dolor abdominal recurrente asociado '
                 'a cambios en la frecuencia o consistencia de las deposiciones, sin causa orgánica demostrable. El '
                 'componente emocional y el estrés son cofactores centrales, no secundarios.',
  'marco_asociado': 'Biomédico (Occidental)',
  'tecnica_asociada': 'BIO-ALO',
  'sintomas': ['dolor abdominal recurrente',
               'alteración tránsito intestinal',
               'distensión',
               'relación con estrés',
               'alivio con defecación'],
  'etiologia': 'Criterios diagnósticos Roma IV: dolor abdominal recurrente al menos 1 día/semana en los últimos 3 '
               'meses, asociado a 2 o más de: relación con defecación, cambio en frecuencia de deposiciones, cambio en '
               'forma o consistencia. Los factores predisponentes incluyen infección gastrointestinal previa (SII '
               'post-infeccioso, 25% de los casos), disbiosis intestinal, estrés psicosocial sostenido, '
               'hipersensibilidad visceral y permeabilidad intestinal aumentada.',
  'mecanismo': 'El eje intestino-cerebro opera bidireccionalmente: el SNC regula la motilidad intestinal mediante el '
               'sistema nervioso entérico, y la microbiota produce el 90% de la serotonina corporal, que impacta '
               'directamente en el estado de ánimo. En el SII hay hipersensibilidad visceral (umbral de dolor '
               'intestinal más bajo que la población general), desregulación de serotonina (receptores 5-HT3 y 5-HT4) '
               'y microinflamación de bajo grado en la mucosa intestinal no detectable por endoscopía estándar.',
  'patron_diagnostico': 'Diagnóstico clínico por criterios Roma IV, sin biomarcador específico. Es fundamental '
                        'descartar: enfermedad inflamatoria intestinal (calprotectina fecal elevada), celiaquía (IgA '
                        'anti-transglutaminasa), cáncer colorrectal (en >45 años o señales de alarma: rectorragia, '
                        'pérdida de peso, anemia). El perfil básico incluye PCR, hemograma, TSH. La presencia de '
                        'síntomas extraintestinales (fatiga, cefalea, vejiga hiperactiva) es característica del SII y '
                        'no debe llevar a buscar causas separadas para cada uno.',
  'protocolo_indicado': 'Primera línea: psicoeducación sobre el eje intestino-cerebro más dieta baja en FODMAP durante '
                        '4-8 semanas. Probióticos: Lactobacillus rhamnosus GG o Bifidobacterium infantis. Psicoterapia '
                        'cognitivo-conductual e hipnoterapia gut-directed tienen evidencia nivel A para SII. Según '
                        'subtipo: SII-D (diarrea predominante): loperamida o rifaximina; SII-C (constipación '
                        'predominante): fibra soluble, linaclotida. Antidepresivos tricíclicos en dosis bajas '
                        '(amitriptilina 10-25mg) para modulación del dolor visceral, independientemente de si hay '
                        'depresión.',
  'contraindicaciones': 'No mantener dieta baja en FODMAP indefinidamente sin supervisión (reduce diversidad de la '
                        'microbiota a largo plazo). No usar antidiarreicos en presencia de fiebre o sangre en heces '
                        '(puede enmascarar infección activa). No omitir el componente psicológico del tratamiento: sin '
                        'gestión del estrés los resultados son parciales.',
  'integracion': 'PSI-PNI: el estrés crónico es cofactor central; la intervención psicológica es tratamiento de '
                 'primera línea, no complemento. BIO-NUT: dieta baja en FODMAP y suplementación con probióticos son '
                 "parte del protocolo estándar. MTC: el patrón de 'Hígado invadiendo Bazo' de la MTC describe con "
                 'precisión la fisiopatología del SII desde otro paradigma.'},
 {'id': 'D08',
  'titulo': 'Bloqueo de Chakra Cardíaco',
  'descripcion': 'Obstrucción del centro energético del corazón que dificulta dar y recibir amor, generando opresión '
                 'en el pecho y aislamiento.',
  'marco_asociado': 'Vibracional / Energético Sutil',
  'tecnica_asociada': 'VIB-REI',
  'sintomas': ['opresión torácica',
               'dificultad para amar',
               'aislamiento',
               'tristeza profunda',
               'sensación de vacío en el pecho'],
  'etiologia': 'El bloqueo del chakra cardíaco (Anahata, cuarto chakra) surge de la acumulación de duelos no '
               "expresados, traiciones afectivas, amor no correspondido, o la decisión inconsciente de 'no volver a "
               "amar' para no sufrir. Según Bruyere ('Wheels of Light'), el chakra cardíaco es el puente entre los "
               'tres chakras inferiores (instintivos) y los tres superiores (espirituales); su bloqueo desconecta '
               'ambas polaridades.',
  'mecanismo': 'El campo electromagnético del corazón es el más extenso del cuerpo humano, irradiando hasta 1.5-3 '
               'metros (HeartMath Institute). El bloqueo del chakra cardíaco se manifiesta como una disminución de la '
               'coherencia cardiaca (medible mediante HRV — Heart Rate Variability). El sistema de Reiki postula que '
               'la energía Universal (Ki) fluye menos a través de las capas del campo cuando hay densidades '
               'emocionales no procesadas en ese centro.',
  'patron_diagnostico': 'Evaluación energética de manos: el terapeuta Reiki entrenado percibe diferencia de '
                        'temperatura y densidad en el área del corazón. Medición de coherencia cardíaca (HRV): baja '
                        'variabilidad indica déficit de regulación del SNA correlacionado. Clínico: opresión en el '
                        'centro del pecho sin causa cardiológica, dificultad para recibir amor o cuidado, tendencia a '
                        'cuidar a todos sin pedir ayuda, sensación de vacío detrás del esternón.',
  'protocolo_indicado': "Protocolo de Reiki para el Chakra Cardíaco (ref. Rand 'The Reiki Touch', posiciones de manos; "
                        "Bruyere 'Wheels of Light', cap. Anahata). Posición de manos: sobre el centro del pecho "
                        '(posición 4 del protocolo clásico Usui Shiki Ryoho), mínimo 5 minutos por posición o hasta '
                        'sentir equilibrio de temperatura. Para la apertura del chakra cardíaco se trabaja también en '
                        'la parte posterior: una mano anterior y una posterior entre las escápulas (área BL-14 a '
                        'BL-15). Símbolo de segundo grado: el símbolo Sei He Ki (mental/emocional) se introduce en el '
                        'chakra cardíaco con intención específica de liberación de patrones emocionales. Sesión '
                        'completa: 60-75 minutos, empezando y terminando en la cabeza (para anclar y cerrar). Práctica '
                        'para casa: mano en el corazón con respiración cuadrada (inhalar 5s, sostener 5s, exhalar 5s, '
                        "sostener 5s), 10 ciclos, con la intención de 'dar y recibir amor en igual medida'. "
                        'Frecuencia: 3-4 sesiones iniciales, semanales o quincenales.',
  'contraindicaciones': 'Reiki no reemplaza la evaluación cardiológica: la opresión torácica debe descartar patología '
                        'cardíaca orgánica antes de abordar solo el nivel energético. No aplicar Reiki directamente '
                        'sobre marcapasos u otros dispositivos electrónicos implantados.',
  'integracion': 'PSI-SOM: la tensión muscular paraescapular y diafragmática que acompaña al bloqueo cardíaco responde '
                 'al trabajo somático de liberación; SE puede preceder o seguir la sesión de Reiki. SOC-CON: si el '
                 'bloqueo está ligado a una pérdida o separación familiar, el trabajo de Constelaciones aborda la raíz '
                 'sistémica. AYU-YOG: el pranayama Bhramari (respiración abeja: exhalar con sonido mmm) tiene efecto '
                 'directo sobre la coherencia cardiaca.'},
 {'id': 'D09',
  'titulo': 'Conflicto de Desvalorización',
  'descripcion': 'Conflicto biológico donde el individuo siente que no es suficiente o que ha fracasado, '
                 'manifestándose en articulaciones y huesos.',
  'marco_asociado': 'Psicosomático (Mente-Cuerpo-Emoción)',
  'tecnica_asociada': 'PSI-BIO',
  'sintomas': ['dolor articular',
               'sensación de fracaso',
               'baja autoestima',
               'comparación constante',
               'rigidez corporal'],
  'etiologia': 'Según la Nueva Medicina Germánica de Hamer y la Biodescodificación de Sabbah, el conflicto de '
               'desvalorización se activa ante un evento-choque donde el individuo siente profundamente que ha '
               'fallado, que es inútil, que no sirve, que no es suficiente. La localización del síntoma depende del '
               'tipo: columna → desvalorización de sí mismo como sostén; articulaciones → desvalorización en relación '
               'a la destreza o función; huesos → desvalorización profunda de la identidad.',
  'mecanismo': "En el modelo de Hamer, el conflicto activa un 'Hamer Herd' (foco cerebral) que controla el tejido "
               "correspondiente: en articulaciones (mesoderma nuevo) el conflicto de desvalorización genera 'necrosis "
               "funcional' del cartílago articular durante la fase activa, que luego intenta repararse en la fase "
               "vagotónica. El síntoma físico es biológicamente coherente con el conflicto emocional (ref. Sabbah 'Le "
               "Descodage Biologique des Maladies', cap. huesos y articulaciones).",
  'patron_diagnostico': 'Historia clínica biológica: identificar el evento-choque específico donde el individuo sintió '
                        "la desvalorización. La frase biológica característica: 'No soy suficiente', 'He fallado en mi "
                        "función', 'No valgo'. Localización: articulaciones (hombros, rodillas, caderas) → "
                        'desvalorización en la función/trabajo; columna → desvalorización de sí mismo como pilar; '
                        'mandíbula → desvalorización de la fuerza o la mordida. Temperatura del síntoma: en fase '
                        'activa el tejido articular puede estar frío; en resolución hay inflamación y calor (señal de '
                        'curación).',
  'protocolo_indicado': "Protocolo de Bioneuroemoción para Conflicto de Desvalorización (ref. Sabbah 'Le Descodage "
                        "Biologique des Maladies'; Enric Corbera 'Bioneuroemoción'). Fase 1 — Identificación del "
                        'conflicto: en sesión, el terapeuta guía con las 4 preguntas diagnósticas: (a) ¿Cuándo comenzó '
                        'exactamente el síntoma? (b) ¿Qué estaba pasando en tu vida en ese momento? (c) ¿Cómo te '
                        'sentiste en ese instante (la emoción biológica, no la historia)? (d) ¿Habías tenido antes una '
                        "emoción similar? Fase 2 — Resignificación: encontrar el sentido biológico del síntoma: '¿Para "
                        "qué me ha servido esta desvalorización? ¿Qué me ha protegido de hacer o de afrontar?' Fase 3 "
                        '— Resolución: el objetivo no es eliminar el síntoma directamente sino resolver el conflicto '
                        'emocional. Una vez resuelto, el cuerpo inicia espontáneamente la fase de reparación (que '
                        'puede incluir inflamación transitoria: es señal de curación). Trabajo entre sesiones: llevar '
                        'un diario donde se registra cuándo se activa la sensación de desvalorización, en qué '
                        'contextos y con qué personas.',
  'contraindicaciones': 'No aplicar el modelo como único abordaje en patología articular grave con componente '
                        'autoinmune (artritis reumatoide, lupus): el manejo médico simultáneo es necesario. No usar el '
                        'modelo para culpabilizar al paciente de su enfermedad: la biología es coherente, no punitiva. '
                        'No omitir la evaluación médica de las articulaciones.',
  'integracion': 'BIO-FIS: el trabajo fisioterapéutico de movilidad articular es complementario y necesario: la '
                 'resolución del conflicto da el permiso para sanar, la fisioterapia facilita la recuperación '
                 'funcional. VIB-RES: el patrón vibracional de desvalorización (D05) y el conflicto biológico son el '
                 'mismo fenómeno abordado desde diferentes paradigmas. SOC-CON: en muchos casos la desvalorización '
                 'tiene raíz en el sistema familiar; las constelaciones abordan la dimensión sistémica.'},
 {'id': 'D10',
  'titulo': 'Trauma Somático No Resuelto',
  'descripcion': 'Experiencia traumática almacenada en el cuerpo que se manifiesta como tensión crónica, '
                 'hipervigilancia y síntomas físicos sin causa orgánica clara.',
  'marco_asociado': 'Psicosomático (Mente-Cuerpo-Emoción)',
  'tecnica_asociada': 'PSI-SOM',
  'sintomas': ['tensión crónica',
               'hipervigilancia',
               'respuesta de sobresalto',
               'disociación corporal',
               'dolor sin causa orgánica'],
  'etiologia': 'El trauma somático surge cuando el sistema nervioso no pudo completar la respuesta de defensa '
               'biológica ante una amenaza (lucha, huida o inmovilización). La energía movilizada por el SNS para '
               "enfrentar la amenaza quedó bloqueada en el cuerpo. Según Levine ('Waking the Tiger'), el trauma no "
               'está en el evento sino en el sistema nervioso que no pudo completar la respuesta adaptativa.',
  'mecanismo': 'El cuerpo almacena la memoria traumática en los músculos, la fascia y la regulación del sistema '
               'nervioso autónomo. El hipocampo (memoria explícita) puede haber procesado cognitivamente el evento, '
               'pero la amígdala (memoria implícita/emocional) y el SNA siguen respondiendo como si el peligro fuera '
               'actual. La hipervigilancia, los sobresaltos exagerados y las contracturas crónicas son signos de un '
               "sistema nervioso que no completó el ciclo de descarga (ref. van der Kolk 'The Body Keeps the Score').",
  'patron_diagnostico': 'Observación del SNA: hiperactivación (taquicardia, respiración superficial, hipervigilancia) '
                        'o hipoactivación (entumecimiento, disociación, parálisis). Mapa corporal: identificar zonas '
                        'de la ventana de tolerancia (Siegel) — cuándo el consultante puede estar presente en el '
                        'cuerpo y cuándo se disocia. Historia de activación: qué situaciones actuales generan '
                        'respuesta desproporcionada (flashback, parálisis, terror). Señales somáticas: temblor '
                        'espontáneo (señal de descarga del SNA), náusea, mareo al abordar ciertas memorias.',
  'protocolo_indicado': "Protocolo de Somatic Experiencing para Trauma Somático (ref. Levine 'In an Unspoken Voice'; "
                        "Payne et al. 'Somatic Experiencing', Frontiers in Psychology 2015). Fase 1 — Titración y "
                        'recursos: el terapeuta NO va directamente al trauma. Primero establece recursos somáticos '
                        '(zonas del cuerpo donde hay seguridad o placer). El trabajo siempre comienza desde el '
                        'recurso. Fase 2 — Pendulación: guiar al consultante a moverse entre el recurso y una pequeña '
                        "dosis de la activación traumática. Técnica: 'Nota X en tu cuerpo (activación)... ahora "
                        "regresa a Y (recurso)... ¿qué notas ahora?' La pendulación entrena al SNA a tolerar la "
                        'activación y volver. Fase 3 — Descarga somática: prestar atención a signos de descarga: '
                        'temblor espontáneo, bostezos profundos, suspiros, cambios de temperatura en las manos. Cuando '
                        'aparecen, el terapeuta los valida y ayuda al consultante a permanecer con ellos. Fase 4 — '
                        'Completar la respuesta biológica: guiar movimientos micro o completos que completan la '
                        "respuesta no completada (levantar un brazo para parar, darse vuelta para 'escapar'). "
                        'Frecuencia: sesiones semanales, aproximadamente 10-20 sesiones para un ciclo completo.',
  'contraindicaciones': 'No hacer trabajo somático de trauma en alguien activamente disociado: la disociación es una '
                        'defensa que se debe respetar antes de trabajar con ella. No acelerar el proceso: el principio '
                        "central es la titración ('poco a poco'). No trabajar trauma severo sin formación certificada "
                        'en SE u otra modalidad somática (TRE, EMDR con componente somático).',
  'integracion': 'PSI-PNI: el SNA y el sistema inmune están directamente interconectados; la resolución del trauma '
                 'mejora también la función inmune y reduce la inflamación de bajo grado. SOC-CON: muchos traumas '
                 'tienen raíz en el campo familiar; las Constelaciones pueden abordar la dimensión sistémica. AYU-YOG: '
                 'el yoga restaurativo (Yoga Nidra, posturas pasivas de apertura) tiene efecto directo sobre el SNP y '
                 'puede complementar las sesiones de SE.'},
 {'id': 'D11',
  'titulo': 'Lealtad Transgeneracional Inconsciente',
  'descripcion': 'Patrón heredado de un ancestro que el individuo repite inconscientemente, generando síntomas que '
                 'pertenecen a la historia familiar no resuelta.',
  'marco_asociado': 'Socio-familiar (Contexto y Sistemas)',
  'tecnica_asociada': 'SOC-GEN',
  'sintomas': ['patrones repetitivos',
               'síntomas sin explicación personal',
               'identificación con un ancestro',
               'destino similar a familiar',
               'culpa inexplicable'],
  'etiologia': "Según Boszormenyi-Nagy ('Invisible Loyalties'), los sistemas familiares mantienen un libro de cuentas "
               'transgeneracional donde se registran las deudas, lealtades y reparaciones pendientes. Un descendiente '
               'puede asumir inconscientemente la misión de reparar lo que no fue resuelto por un ancestro: repetir su '
               'destino, enfermarse donde él se enfermó, o morir a la misma edad.',
  'mecanismo': 'El epigenoma registra experiencias de estrés extremo (guerra, hambre, trauma masivo) y estas marcas se '
               'transmiten a la siguiente generación (Yehuda et al., estudios sobre PTSD en hijos de sobrevivientes '
               'del Holocausto). En el nivel psicológico, la transmisión ocurre a través de los relatos implícitos de '
               'la familia, los silencios significativos, los nombres que se repiten. El genosociograma de McGoldrick '
               "mapea estos patrones visualmente (ref. McGoldrick 'Genograms', cap. 2-3).",
  'patron_diagnostico': 'Genograma de 3 generaciones: identificar patrones de enfermedad, muertes tempranas, '
                        "tragedias, ausencias, secretos. Preguntas diagnósticas: '¿Murió alguien importante en tu "
                        "familia a esta edad o en esta circunstancia?' '¿Hay alguien en tu familia de quien no se "
                        "habla?' '¿Hay nombres que se repiten?' Síntomas que apuntan a lealtad transgeneracional: "
                        'síntoma que comenzó en la misma edad en que sucedió algo importante a un ancestro; síntoma '
                        "que 'no tiene sentido' desde la historia personal del consultante.",
  'protocolo_indicado': 'Protocolo de Terapia Narrativa Familiar y Genograma para Lealtades Transgeneracionales (ref. '
                        "McGoldrick 'Genograms'; White & Epston 'Narrative Means to Therapeutic Ends'; "
                        "Boszormenyi-Nagy 'Invisible Loyalties'). Fase 1 — Construcción del genograma: 3 generaciones "
                        'mínimo, incluyendo: fechas de nacimiento y muerte, causas de muerte, enfermedades '
                        'importantes, migraciones, guerras, pérdidas de patrimonio, secretos. El terapeuta presta '
                        'especial atención a coincidencias de fechas y patrones repetitivos. Fase 2 — Identificación '
                        'de la lealtad: identificar con qué ancestro el consultante está en lealtad. Pregunta clave: '
                        "'¿Hay alguien en tu árbol que haya vivido algo parecido a lo que tú estás viviendo?' Fase 3 — "
                        'Trabajo de deslealtad reparativa (White & Epston): el consultante escribe una carta al '
                        "ancestro identificado: 'Yo te veo. Lo que te pasó fue real. Yo lo cargo para ti porque te "
                        "amo. Pero ahora te devuelvo tu destino con amor y me quedo con el mío.' Fase 4 — Ritual de "
                        'cierre: quemar la carta, plantar algo, crear un objeto que represente el nuevo capítulo.',
  'contraindicaciones': 'No explorar lealtades transgeneracionales sin vínculo terapéutico sólido: el material puede '
                        'ser muy movilizador. No trabajar con secretos familiares que involucren a terceros vivos sin '
                        'considerar el impacto relacional. No imponer una interpretación: el terapeuta propone, el '
                        'consultante reconoce.',
  'integracion': 'SOC-CON: las Constelaciones Familiares son otra vía de acceso al mismo campo; la diferencia es que '
                 'el Genograma usa el lenguaje y la narración, las Constelaciones usan el movimiento espacial. '
                 "PSI-BIO: la biodescodificación identifica el 'conflicto biológico' que el ancestro no pudo resolver "
                 'y que el descendiente carga — estos paradigmas son complementarios. PSI-SOM: el trauma '
                 'transgeneracional tiene sustrato en el SNA; el trabajo somático puede liberar lo que el trabajo '
                 'cognitivo o narrativo no alcanza.'},
 {'id': 'D12',
  'titulo': 'Acumulación de Ama (Toxinas Ayurvédicas)',
  'descripcion': 'Acumulación de toxinas metabólicas y energéticas por digestión deficiente, generando pesadez, '
                 'nublamiento mental y acumulación tisular.',
  'marco_asociado': 'Ayurveda',
  'tecnica_asociada': 'AYU-PAN',
  'sintomas': ['pesadez corporal',
               'lengua saburral',
               'nublamiento mental',
               'congestión nasal crónica',
               'retención líquidos'],
  'etiologia': "El Ama (literalmente 'crudo', 'no digerido') se acumula cuando el Agni (fuego digestivo) está "
               'debilitado. Sus causas principales: comer antes de que la comida anterior haya sido digerida, '
               'alimentos incompatibles (Viruddha Ahara: leche con pescado, miel calentada, frutas con lácteos), '
               "horarios irregulares, estrés sostenido que apaga el Agni, y emociones no procesadas (la 'digestión' en "
               "Ayurveda incluye la digestión emocional) (ref. Lad 'Textbook of Ayurveda Vol.3', cap. Panchakarma).",
  'mecanismo': 'El Ama es una toxina densa, pegajosa y fría (lo opuesto al Agni que es ligero, caliente y claro). El '
               'Ama obstruye los Srotamsi (canales corporales): cuando obstruye el Rasa Dhatu (tejido de '
               'plasma/nutrición), genera pesadez y congestión; cuando obstruye la mente (Manas), genera nublamiento '
               'mental y confusión. La lengua saburral es la manifestación visible del Ama en el tracto digestivo.',
  'patron_diagnostico': 'La lengua es el principal mapa de diagnóstico del Ama: capa blanca gruesa y pegajosa sobre '
                        'toda la superficie indica Ama en el tracto digestivo. Capa amarilla sugiere Ama-Pitta (Ama '
                        'caliente). Signos adicionales: aliento con olor extraño en ayunas, evacuaciones malolientes o '
                        'de alta flotabilidad (gas intestinal), pesadez generalizada especialmente al despertar, '
                        'inflamación de articulaciones con rigidez matinal, congestión nasal crónica, orina turbia.',
  'protocolo_indicado': "Protocolo de Panchakarma para Ama (ref. Lad 'Textbook of Ayurveda Vol.3'; Frawley 'Ayurvedic "
                        "Healing', cap. Detox). Fase 1 — Preparación / Purvakarma (3-7 días): Snehana (oleación "
                        'interna): ghee clarificado en dosis crecientes (comenzar con 1-2 cucharadas en ayunas, '
                        'aumentar gradualmente a 4-6) para lubricar el canal digestivo y movilizar el Ama. Swedana '
                        '(sudación): baño de vapor herbal para abrir los poros y facilitar la eliminación. Dieta: '
                        'monodieta de kichadi (arroz basmati + lentejas + ghee + especias digestivas: jengibre, '
                        'comino, cilantro). Fase 2 — Purificación principal (según tipo de Ama): Vata aggravado → '
                        'Basti (enemas de aceite de sésamo + hierbas). Pitta aggravado → Virechana (purga terapéutica '
                        'con Triphala o aceite de ricino). Kapha con congestión → Nasya (aceite de sésamo nasal) + '
                        'Vamana (emesis terapéutica, solo bajo supervisión de vaidya calificado). Fase 3 — '
                        'Rejuvenecimiento / Rasayana: una vez eliminado el Ama, fase de nutrición profunda. '
                        'Chyawanprash 1 cucharadita con leche tibia mañana y noche; Ashwagandha, Shatavari. Duración: '
                        '3-5 días para limpieza básica; 21-28 días para ciclo completo.',
  'contraindicaciones': 'El Panchakarma completo requiere supervisión de un vaidya (médico ayurvédico) calificado. No '
                        'aplicar Vamana o Virechana en personas débiles, embarazadas, menores o ancianos sin '
                        'experiencia clínica. No iniciar Panchakarma sin Purvakarma: sin preparación previa la '
                        'purificación puede ser excesiva y dañina.',
  'integracion': 'BIO-NUT: la disbiosis intestinal (D18) y el Ama son frecuentemente co-existentes; el protocolo de 4 '
                 'fases de BIO-NUT y el Panchakarma son complementarios y pueden secuenciarse. MTC-FIT: la Deficiencia '
                 'de Qi de Bazo (D06) es el correlato MTC del Agni manda — ambas tradiciones convergen en la '
                 "importancia del fuego digestivo. PSI-BIO: la 'digestión emocional' del Ayurveda tiene correlato en "
                 "el concepto biodescodificativo de 'no poder digerir' o aceptar situaciones."},
 {'id': 'D13',
  'titulo': 'Disregulación del Eje HPA (Estrés Crónico)',
  'descripcion': 'Alteración del eje hipotálamo-hipófisis-adrenal por estrés sostenido, generando fatiga suprarrenal, '
                 'insomnio y desregulación inmunitaria.',
  'marco_asociado': 'Psicosomático (Mente-Cuerpo-Emoción)',
  'tecnica_asociada': 'PSI-PNI',
  'sintomas': ['fatiga que no cede con descanso',
               'insomnio',
               'infecciones frecuentes',
               'antojos salados/dulces',
               'hipotensión ortostática'],
  'etiologia': 'La disregulación del eje HPA resulta de la activación repetida y sostenida de la respuesta al estrés '
               'sin recuperación suficiente. El cuerpo humano fue diseñado para el estrés agudo (el tigre); el estrés '
               'crónico moderno (presiones laborales, conflictos relacionales, amenaza económica sostenida) mantiene '
               'el sistema en alerta permanente, agotando las adrenales y desregulando el ritmo circadiano del '
               "cortisol (ref. Sapolsky 'Why Zebras Don't Get Ulcers', cap. 13-14).",
  'mecanismo': 'El eje HPA opera como un termostato: el cortisol producido por las adrenales inhibe por '
               'retroalimentación negativa la secreción de CRH hipotalámico y ACTH hipofisario. Con el estrés crónico, '
               'los receptores de glucocorticoides del hipocampo (que median la retroalimentación) se reducen '
               '(downregulation), el freno falla, y el cortisol se mantiene elevado. El cortisol crónico: destruye '
               'neuronas del hipocampo (memoria deteriorada), suprime la síntesis de colágeno (cicatrización lenta), '
               "inhibe la función tiroidea periférica (fatiga), e inhibe el sistema reproductivo (McEwen 'The End of "
               "Stress as We Know It').",
  'patron_diagnostico': 'Gold standard: cortisol en saliva en 4 puntos del día (07:00, 12:00, 17:00, 22:00). Patrón '
                        'normal: pico matinal (CAR: Cortisol Awakening Response) con descenso vespertino. En '
                        'disregulación HPA: pico matinal aplanado o ausente, valores nocturnos elevados, curva '
                        'invertida. Clínicamente: fatiga matinal (más cansados al despertar que al acostarse), segundo '
                        'viento nocturno (activación después de las 21h), antojos de salado y azúcar, presión arterial '
                        'baja al levantarse, infecciones frecuentes.',
  'protocolo_indicado': "Protocolo de PNI para Disregulación HPA (ref. Sapolsky 'Why Zebras Don't Get Ulcers'; McEwen "
                        "'The End of Stress as We Know It'; HeartMath Institute). Pilar 1 — Ciclo sueño-vigilia: fijar "
                        'hora de despertar constante (más importante que la hora de acostarse para resetear el CAR); '
                        'luz solar directa en los primeros 30 minutos del día (activa el ritmo circadiano del '
                        'cortisol); oscuridad total para dormir; temperatura ambiental 18-20°C. Pilar 2 — Modulación '
                        'del cortisol: adaptógenos con evidencia: Ashwagandha (KSM-66, 600mg/día) reduce el cortisol '
                        'matinal en ensayos clínicos; Rhodiola rosea 200-400mg (normaliza el ritmo HPA por acción en '
                        'los receptores de glucocorticoides); Magnesio glicinato o treonato 300-400mg/día (cofactor '
                        'para la enzima que sintetiza cortisol y para la melatonina). Pilar 3 — Down-regulation del '
                        'SNA: respiración diafragmática 5-7 respiraciones por minuto activa el reflejo de '
                        'Hering-Breuer y reduce el cortisol en 10-15 minutos; yoga nidra (30 min equivale a 4h de '
                        'sueño en EEG); NSDR (Non-Sleep Deep Rest, protocolos de Huberman). Pilar 4 — Alimentación: no '
                        'saltarse el desayuno (el cortisol matinal en ayunas se eleva aún más); proteína en el '
                        'desayuno > carbohidratos refinados; limitar cafeína después de las 13h.',
  'contraindicaciones': 'No prescribir Ashwagandha en personas con tiroiditis de Hashimoto sin control médico (puede '
                        'exacerbar la respuesta autoinmune en algunos casos). No interrumpir bruscamente '
                        'glucocorticoides farmacológicos. Rhodiola está contraindicada en embarazo.',
  'integracion': 'MTC-FIT: la Deficiencia de Qi de Bazo (D06) y la Deficiencia de Yin de Riñón (D14) son los '
                 'correlatos MTC más frecuentes de la disregulación HPA. AYU: el agotamiento suprarrenal correlaciona '
                 'con el concepto de Ojas agotado (vitalidad profunda) del Ayurveda. BIO-NUT: la suplementación de '
                 'micronutrientes (zinc, vitamina D, B5 para las adrenales, vitamina C) es parte inseparable del '
                 'protocolo.'},
 {'id': 'D15',
  'titulo': 'Desequilibrio de Dosha Kapha',
  'descripcion': 'Exceso del dosha Kapha (tierra/agua) que genera acumulación, lentitud, apego y congestión en '
                 'múltiples niveles.',
  'marco_asociado': 'Ayurveda',
  'tecnica_asociada': 'AYU-YOG',
  'sintomas': ['letargo',
               'congestión crónica',
               'apego excesivo',
               'aumento peso',
               'somnolencia diurna',
               'retención líquidos'],
  'etiologia': 'El exceso de Kapha (dosha tierra-agua) se genera por: sedentarismo, sueño excesivo, alimentación '
               'pesada y fría (lácteos, trigo, azúcar, carnes rojas), apego emocional crónico, falta de estimulación '
               'mental y ejercicio. El Kapha es el dosha que necesita ser desafiado para equilibrarse: el confort y la '
               "comodidad en exceso lo incrementan (ref. Lad 'Textbook of Ayurveda Vol.1', cap. 7).",
  'mecanismo': 'El exceso de Kapha genera acumulación y obstrucción de los srotamsi: el canal respiratorio se congesta '
               '(mucosidad crónica, sinusitis, asma tipo Kapha), el canal digestivo se vuelve lento (hipoclorhidria, '
               'estreñimiento blando), el sistema circulatorio se hace más denso (colesterol LDL elevado). A nivel '
               'mental: pensamiento lento, memoria densa pero lenta para activar, tendencia a la depresión pesada y '
               'quieta (diferente de la depresión Vata: ansiosa y agitada).',
  'patron_diagnostico': 'Kapha en exceso: lengua con capa blanca gruesa y húmeda, pulso lento, suave y profundo, piel '
                        'pálida, fría y húmeda. Constitución física: tendencia al sobrepeso con distribución en '
                        'caderas y abdomen, estructura ósea grande. Patrón emocional: apego, dificultad para cambiar, '
                        'somnolencia. Digestión: sensación de pesadez después de comer, digestión muy lenta (puede '
                        'tardar 4-6h para sentir hambre después de una comida mediana).',
  'protocolo_indicado': "Protocolo de Yoga y Pranayama para Kapha aggravado (ref. Frawley 'Yoga and Ayurveda', cap. 8; "
                        "Lad 'Textbook of Ayurveda Vol.1', cap. 7). Yoga: práctica dinámica y estimulante (lo opuesto "
                        'al Kapha sedentario). Secuencias indicadas: Surya Namaskar (Saludo al Sol) a ritmo rápido, '
                        '5-10 rondas matutinas; posturas de torsión (Ardha Matsyendrasana, Parivrtta Trikonasana) para '
                        'estimular el Agni y drenar la congestión; posturas invertidas (Sarvangasana, Halasana) para '
                        'drenar mucosidades y estimular la glándula tiroides. Pranayama específico para Kapha: '
                        'Bhastrika (respiración fuelle): 3 series de 20-30 respiraciones vigorosas — el pranayama más '
                        'indicado para Kapha por ser calórico, movilizador y secante; Kapalabhati (respiración del '
                        'cráneo brillante): 1-3 minutos por la mañana en ayunas. Dieta y estilo de vida: levantarse '
                        'antes del amanecer (idealmente a las 6am), evitar la siesta, alimentos secos, calientes y '
                        'ligeros (legumbres, verduras de hoja verde, jengibre, pimienta negra, mostaza). Hierbas: '
                        'Trikatu (jengibre seco + pimienta negra + pimienta larga) 500mg antes de las comidas para '
                        'encender el Agni.',
  'contraindicaciones': 'Bhastrika y Kapalabhati contraindicados en embarazo, hipertensión no controlada, enfermedades '
                        'cardíacas, hernias abdominales, epilepsia. No practicar estas técnicas durante la '
                        'menstruación.',
  'integracion': 'BIO-NUT: el exceso de Kapha correlaciona frecuentemente con resistencia a la insulina, '
                 'hipotiroidismo e hiperlipidemia — evaluar analíticamente. MTC: el Kapha en exceso tiene cierta '
                 "semejanza con la 'Humedad y Flema' de la MTC (aunque los paradigmas no son equivalentes). PSI-PNI: "
                 'la depresión tipo Kapha puede tener sustrato en hipotiroidismo y déficit de dopamina — explorar '
                 'biológicamente antes de concluir que es solo de origen dóshico.'},
 {'id': 'D16',
  'titulo': 'Patrón de Frecuencia de Miedo',
  'descripcion': 'Resonancia energética dominada por la frecuencia del miedo, que afecta riñones, vejiga y sistema '
                 'nervioso, generando inseguridad profunda.',
  'marco_asociado': 'Vibracional / Energético Sutil',
  'tecnica_asociada': 'VIB-SON',
  'sintomas': ['miedo crónico', 'inseguridad', 'dolor lumbar bajo', 'micción frecuente', 'temblores'],
  'etiologia': 'El miedo crónico como estado de resonancia predominante se instala cuando las experiencias de amenaza '
               "se repiten con la suficiente frecuencia como para convertirse en el 'tono de base' del sistema "
               'nervioso. En el paradigma vibracional, el miedo tiene una frecuencia específica que el cuerpo aprende '
               'a reproducir. El miedo como frecuencia dominante afecta el campo energético en la zona de los riñones '
               'y la vejiga (correlato de la MTC: el Riñón es el órgano del agua y el miedo es su emoción).',
  'mecanismo': 'Según la Cymatics (Jenny, 1967), las frecuencias sonoras organizan la materia: frecuencias armónicas '
               'generan patrones coherentes; frecuencias discordantes generan patrones caóticos. Aplicado al cuerpo, '
               'un campo bioenergético dominado por la frecuencia del miedo genera incoherencia en los patrones de '
               "resonancia celular. Beaulieu ('Music and Sound in the Healing Arts') propone que los intervalos "
               'armónicos (quinta justa 3:2, octava 2:1) tienen efecto directo sobre el sistema nervioso y que las '
               'frecuencias de baja vibración pueden ser gradualmente desplazadas por frecuencias más armónicas.',
  'patron_diagnostico': 'Evaluación vibratoria: el terapeuta de sonido percibe en el campo del cuenco tibetano o '
                        "diapasón una 'rugosidad' o falta de resonancia en el área lumbar-sacra cuando hay miedo "
                        'crónico. Kinesiología aplicada: test del músculo psoas-ilíaco (el miedo se almacena '
                        'frecuentemente en el psoas). Clínico: insomnio por hipervigilancia nocturna, dolor lumbar '
                        'bajo sin causa estructural, micción frecuente bajo estrés, temblores finos en situaciones de '
                        'exposición, contracción involuntaria del periné.',
  'protocolo_indicado': "Protocolo de Terapia de Sonido para Patrón de Frecuencia de Miedo (ref. Beaulieu 'Music and "
                        "Sound in the Healing Arts'; Goldman 'Healing Sounds: The Power of Harmonics'). Cuencos "
                        "tibetanos: cuenco en clave de 'F' (Fa) — frecuencia asociada al chakra sacro y riñones. El "
                        'terapeuta comienza el cuenco alejado del cuerpo y lo acerca gradualmente a la zona '
                        'lumbar-sacra mientras el consultante está en decúbito supino. El movimiento del cuenco genera '
                        "una ola de sonido que 'barre' la frecuencia del miedo. Diapasones: Ohm tuning forks (136.1 "
                        'Hz, frecuencia Om/tierra): se aplican a puntos acupunturales de Riñón (KI-1 Yong Quan en la '
                        'planta del pie, KI-3 Tai Xi en el tobillo medial). Esta frecuencia tiene efecto de grounding '
                        '(enraizamiento) — el contrapunto al miedo es la seguridad. Sesión completa: 45-60 minutos, '
                        'consultante en decúbito supino, ojos cerrados. El terapeuta trabaja con cuencos, diapasones y '
                        'voz (armónicos). Tarea para casa: escuchar 20 min diarios de música con quinta justa (música '
                        'barroca, canto gregoriano, grabaciones con OM) — la quinta justa (3:2) es el intervalo más '
                        'estudiado por efecto ansiolítico.',
  'contraindicaciones': 'No usar cuencos tibetanos sobre el cuerpo en personas embarazadas (especialmente primer '
                        'trimestre). No trabajar con sonido de alta intensidad cerca de los oídos en personas con '
                        'hiperacusia o tinnitus. El trabajo con el miedo puede reactivar memorias traumáticas — tener '
                        'protocolo de contención.',
  'integracion': 'PSI-SOM: el miedo como patrón frecuencial tiene base somática en el SNS — el trabajo de Somatic '
                 'Experiencing puede liberar el miedo a nivel nervioso de forma complementaria. MTC-ACU: el meridiano '
                 'de Riñón y Vejiga (meridiano del miedo en MTC) puede tratarse con acupuntura en paralelo. PSI-PNI: '
                 'el cortisol crónico del miedo tiene efectos medibles en el sistema inmune y el hipocampo — el '
                 'abordaje vibracional puede complementar el protocolo de PNI.'},
 {'id': 'D17',
  'titulo': 'Síndrome de Sobrecarga del Cuidador',
  'descripcion': 'Agotamiento físico y emocional por asumir el rol de cuidador sin límites, descuidando la propia '
                 'salud y necesidades.',
  'marco_asociado': 'Socio-familiar (Contexto y Sistemas)',
  'tecnica_asociada': 'SOC-ANT',
  'sintomas': ['agotamiento',
               'descuido personal',
               'culpa por descanso',
               'tensión mandibular',
               'insomnio',
               'irritabilidad'],
  'etiologia': 'El Síndrome de Sobrecarga del Cuidador (Caregiver Burnout) surge cuando el rol de cuidado se ejerce de '
               'forma continuada sin reciprocidad, sin descanso y sin reconocimiento. Las personas que cuidan a '
               'familiares con enfermedades crónicas tienen hasta 3 veces más riesgo de depresión y 2 veces más riesgo '
               'de problemas cardiovasculares (Kiecolt-Glaser et al.). El componente cultural es central: en muchas '
               'culturas latinoamericanas el rol del cuidador (generalmente la mujer) es mandatorio e invisibilizado '
               "(ref. Kleinman 'The Illness Narratives').",
  'mecanismo': 'El cuidado sin límites activa crónicamente la respuesta de estrés (eje HPA, SNS) mientras suprime el '
               'sistema de recompensa propio: el cuidador pospone permanentemente sus propias necesidades. La '
               "'compasión fatiga' resulta de la activación repetida de la empatía sin regulación emocional propia. "
               'Kleinman describe cómo la narrativa cultural del sacrificio patologiza al cuidador: el sufrimiento del '
               "cuidador se hace invisible e incluso se refuerza culturalmente (ref. Engel 'The Need for a New Medical "
               "Model').",
  'patron_diagnostico': 'Escala de Zarit (Burden Interview): 22 ítems validados que cuantifican la carga objetiva y '
                        'subjetiva del cuidador. Historia: ¿Cuánto tiempo lleva en el rol de cuidador? ¿Tiene relevo? '
                        '¿Cuándo fue la última vez que hizo algo solo/a para sí mismo/a? ¿Siente culpa cuando '
                        'descansa? Síntomas físicos: tensión mandibular, insomnio fragmentado, cefalea tensional, '
                        'herpes recurrente (reactivación por estrés), dolor lumbar.',
  'protocolo_indicado': "Protocolo de Ecología Social para Cuidador Sobrecargado (ref. Kleinman 'The Illness "
                        "Narratives', cap. cuidadores; Engel 'The Need for a New Medical Model'). Pilar 1 — "
                        'Reconocimiento cultural: primer paso terapéutico es hacer visible lo invisible: nombrar que '
                        'cuidar tiene un costo físico y emocional real, que ese costo es legítimo, y que la salud del '
                        'cuidador no es secundaria a la del cuidado. Validación sin culpa. Pilar 2 — Mapeo de red de '
                        'apoyo: usar el ecomapa (herramienta de trabajo social) para identificar quién más podría '
                        'asumir parte del cuidado. Construcción de red: familia extendida, vecinos, grupos de apoyo, '
                        'instituciones. Pilar 3 — Plan de descanso concreto: planificar, con el apoyo de la red, '
                        'períodos de descanso mínimos (2h al día completamente libres, 1 día al mes). No como '
                        "'permiso' sino como prescripción terapéutica. Pilar 4 — Trabajo de límites: terapia "
                        'individual o grupal (grupos de cuidadores) con herramienta de comunicación no violenta '
                        "(Rosenberg): 'Observación + Sentimiento + Necesidad + Pedido'. Pilar 5 — Autocuidado básico: "
                        'ejercicio (15-30 min caminata diaria), alimentación regular, contacto social propio (no en '
                        'rol de cuidador).',
  'contraindicaciones': 'No iniciar trabajo de límites profundos en un cuidador en crisis aguda: primero estabilizar. '
                        'No sugerir abandonar el rol de cuidado sin evaluar el impacto familiar y cultural: la culpa '
                        'puede ser más dañina que el agotamiento. No abordar solo el componente individual sin '
                        'explorar el sistema familiar que sostiene el patrón.',
  'integracion': 'PSI-PNI: el estrés crónico del cuidador tiene correlatos medibles en cortisol, telómeros y sistema '
                 'inmune — el abordaje de PNI puede objetivar la gravedad. SOC-CON: las Constelaciones Familiares '
                 'pueden revelar por qué esta persona asumió el rol de cuidador en el sistema (lealtad sistémica, '
                 'mandato). PSI-SOM: el agotamiento del cuidador tiene sustrato somático en el SNA; el trabajo '
                 'corporal puede liberar la tensión acumulada.'},
 {'id': 'D18',
  'titulo': 'Disbiosis Intestinal con Componente Emocional',
  'descripcion': 'Desequilibrio en la composición y función de la microbiota intestinal que se sostiene y amplifica '
                 'por factores emocionales, generando síntomas digestivos crónicos entrelazados con cambios en el '
                 'estado de ánimo, la energía y la claridad mental. La disbiosis y el estado emocional se '
                 'retroalimentan mutuamente a través del eje intestino-cerebro.',
  'marco_asociado': 'Biomédico (Occidental)',
  'tecnica_asociada': 'BIO-NUT',
  'sintomas': ['distensión abdominal',
               'alternancia ánimo/digestión',
               'antojos azúcar',
               'fatiga postprandial',
               'intolerancias alimentarias'],
  'etiologia': 'La disbiosis se origina por: uso de antibióticos o inhibidores de bomba de protones (IBP) crónicos, '
               'dieta alta en ultraprocesados y azúcares refinados, estrés crónico (el cortisol altera directamente la '
               'composición de la microbiota), parto por cesárea o falta de lactancia materna como antecedentes. La '
               'conexión emocional opera vía eje intestino-cerebro: el estrés modifica la microbiota, y la microbiota '
               'alterada produce metabolitos que afectan el estado de ánimo, creando un ciclo de retroalimentación.',
  'mecanismo': 'La reducción de diversidad bacteriana disminuye la producción de ácidos grasos de cadena corta (AGCC: '
               'butirato, propionato, acetato), que son el principal alimento de los colonocitos y tienen efecto '
               "antiinflamatorio sistémico. La permeabilidad intestinal aumentada ('leaky gut') permite el paso de "
               'lipopolisacáridos bacterianos (LPS) a la circulación, activando una inflamación sistémica de bajo '
               'grado que se manifiesta como fatiga, niebla mental y depresión. El 95% de la serotonina corporal se '
               'produce en el intestino; la disbiosis altera esta producción.',
  'patron_diagnostico': 'Historia detallada de uso de antibióticos, hábitos alimentarios y nivel de estrés sostenido. '
                        'Marcadores de laboratorio: calprotectina fecal (inflamación intestinal), zonulina sérica '
                        '(permeabilidad intestinal), PCR ultrasensible e IL-6 (inflamación sistémica). Test de aliento '
                        'con H2 para descartar SIBO (sobrecrecimiento bacteriano intestinal, que puede coexistir). '
                        'Analítica nutricional: vitamina D, zinc, ferritina, B12 (frecuentemente bajos en disbiosis '
                        'crónica).',
  'protocolo_indicado': 'Protocolo de 4 fases: (1) Eliminación: retirar azúcares, ultraprocesados y alimentos FODMAP '
                        'durante 4-6 semanas. (2) Reparación de mucosa: L-glutamina 5g/día, zinc, vitamina D3, Omega-3 '
                        'y caldo de hueso. (3) Reinoculación: probióticos multicepa (Lactobacillus acidophilus + '
                        'Bifidobacterium longum) con prebióticos (inulina, almidón resistente). (4) Mantenimiento: '
                        'dieta mediterránea y gestión activa del estrés como pilar permanente.',
  'contraindicaciones': 'No iniciar prebióticos si hay SIBO activo sin tratarlo primero (los prebióticos alimentan el '
                        'sobrecrecimiento). No prescribir L-glutamina en personas con antecedentes de convulsiones o '
                        'neoplasias activas. No eliminar grupos alimentarios indefinidamente sin seguimiento '
                        'nutricional.',
  'integracion': 'PSI-PNI: la gestión del estrés es parte inseparable del protocolo; sin ella la disbiosis recurre. '
                 'BIO-ALO: puede requerir rifaximina si se confirma SIBO. AYU: el concepto de Ama (toxinas por '
                 'digestión deficiente) y Agni manda (fuego digestivo débil) del Ayurveda describe este mismo patrón '
                 'desde otro paradigma, con protocolos complementarios.'},
 {'id': 'D20',
  'titulo': 'Conflicto de Territorio',
  'descripcion': 'Conflicto biológico relacionado con la sensación de no tener espacio propio, ser invadido o no poder '
                 'establecer límites.',
  'marco_asociado': 'Psicosomático (Mente-Cuerpo-Emoción)',
  'tecnica_asociada': 'PSI-BIO',
  'sintomas': ['tensión hombros/cuello',
               'necesidad de espacio',
               'irritabilidad en lugares cerrados',
               'dermatitis',
               'dificultad para poner límites'],
  'etiologia': 'Según Hamer y Sabbah, el conflicto de territorio se activa cuando el individuo siente que su espacio '
               'vital está siendo invadido o que no puede establecer ni defender sus límites. La variante masculina y '
               'femenina difieren: el hombre siente que alguien invade su territorio (su pareja, su puesto, su casa); '
               'la mujer siente que no puede entrar o establecerse en un territorio (ser excluida de un grupo, no '
               'poder entrar en una casa). Las vías biológicas afectadas son la piel (límite entre el yo y el mundo) y '
               'la musculatura de hombros y cuello.',
  'mecanismo': 'La piel (epidermis, capas superficiales) tiene origen ectodérmico y responde a los conflictos de '
               'contacto/separación y territorio. El conflicto de territorio activa una respuesta en la fase activa '
               'que puede manifestarse como dermatitis, eccema o psoriasis. La musculatura de hombros y cuello, que '
               "corresponde al área de 'carga' y 'defensa', responde al conflicto con hipertonía crónica — una "
               "preparación para una defensa que nunca llega (ref. Sabbah 'Le Descodage Biologique des Maladies', cap. "
               'piel y territorio).',
  'patron_diagnostico': 'Historia: identificar si hubo un evento-choque donde el individuo sintió que alguien invadía '
                        'su espacio o donde el individuo no pudo marcar sus límites. Frase biológica característica: '
                        "'¡Que no me invadan!', '¡No pueden entrar aquí!', 'No tengo espacio para mí'. Síntomas: "
                        "dermatitis en la zona de 'límite' (manos: relación con objetos y personas; cara: identidad), "
                        'tensión crónica de hombros y cuello, irritabilidad en espacios cerrados, necesidad frecuente '
                        'de espacio propio.',
  'protocolo_indicado': "Protocolo de Bioneuroemoción para Conflicto de Territorio (ref. Sabbah 'Le Descodage "
                        "Biologique des Maladies'; Corbera 'Bioneuroemoción'). Fase 1 — Identificación: encontrar el "
                        'evento-choque con las 4 preguntas diagnósticas: (a) ¿Cuándo comenzó exactamente el síntoma? '
                        '(b) ¿Qué estaba pasando en tu vida en ese momento? (c) ¿Cómo te sentiste en ese instante (la '
                        'emoción biológica)? (d) ¿Habías tenido antes una emoción similar? Fase 2 — Localización '
                        'biológica: la localización de la dermatitis o la tensión muscular da información sobre el '
                        'tipo de conflicto específico. Manos: relación con el trabajo y objetos; cara: identidad y '
                        'cómo me muestro al mundo; hombros: carga y responsabilidad. Fase 3 — Trabajo de límites: el '
                        'objetivo terapéutico es que el individuo pueda establecer límites de forma directa y verbal, '
                        'en lugar de que el cuerpo lo haga a través de la piel o los músculos. Técnica: role playing '
                        'de situaciones donde habitualmente cede el límite; trabajo con la voz (la voz es el primer '
                        'instrumento de límite). Fase 4 — Resignificación: el síntoma en la piel puede resignificarse '
                        "como 'la piel está aprendiendo a marcar qué es mío y qué no es mío'.",
  'contraindicaciones': 'No aplicar el modelo como única intervención en dermatitis activa severa con infección '
                        'secundaria: requiere manejo dermatológico en paralelo. No culpabilizar al paciente de su '
                        'síntoma. No trabajar el conflicto de invasión con el agresor presente en la consulta sin un '
                        'encuadre terapéutico claro.',
  'integracion': 'BIO-ALO: la dermatitis y el eccema requieren evaluación dermatológica y en casos severos, '
                 'tratamiento médico — el abordaje biológico trabaja la raíz. SOC-CON: el conflicto de no poder poner '
                 'límites frecuentemente tiene raíces en el sistema familiar (en la familia de origen, los límites '
                 'tampoco estaban claros). BIO-FIS: la tensión de hombros y cuello responde a fisioterapia y '
                 'liberación miofascial, que puede complementar el trabajo biológico.'},
 {'id': 'D21',
  'titulo': 'Desalineación del Campo Electromagnético Corporal',
  'descripcion': 'Alteración del campo bioelectromagnético del cuerpo por exposición a frecuencias artificiales o '
                 'desequilibrios energéticos internos.',
  'marco_asociado': 'Vibracional / Energético Sutil',
  'tecnica_asociada': 'VIB-SON',
  'sintomas': ['cefalea electromagnética',
               'insomnio por dispositivos',
               'sensibilidad a campos eléctricos',
               'zumbido oídos',
               'agitación sin causa'],
  'etiologia': 'La desalineación del campo bioelectromagnético surge de la exposición sostenida a campos '
               'electromagnéticos artificiales (EMF: wi-fi, teléfonos móviles, ordenadores, líneas de alta tensión), '
               'sumada a una pérdida del contacto con la frecuencia natural de la Tierra (Resonancia Schumann: 7.83 '
               'Hz). La OMS reconoce que entre el 1-3% de la población reporta síntomas atribuidos a EMF '
               '(hipersensibilidad electromagnética, EHS) aunque no hay consenso sobre su mecanismo (ref. Oschman '
               "'Energy Medicine').",
  'mecanismo': 'El cuerpo humano tiene su propio campo electromagnético complejo: el corazón genera el campo más '
               'fuerte (1.5-3m, medible con magnetocardiograma), el cerebro genera ondas electromagnéticas medibles '
               '(EEG), y cada célula tiene un potencial de membrana eléctrico. La Resonancia Schumann (7.83 Hz) '
               'coincide con la frecuencia alfa del cerebro humano en estado relajado: la desconexión de la Tierra '
               '(por vivir en edificios, con calzado sintético) priva al SNA de esta frecuencia de sincronización '
               "(ref. Tiller 'Science and Human Transformation').",
  'patron_diagnostico': 'Evaluación clínica: historia de síntomas que empeoran en ambientes con alta densidad de '
                        'dispositivos electrónicos y mejoran en espacios naturales (bosque, playa, campo). Síntomas: '
                        'cefalea que mejora alejándose de dispositivos, zumbido en oídos sin causa audiológica, '
                        'insomnio que empeora con el teléfono cerca de la cama, fatiga inexplicada en ambientes '
                        'cerrados con muchos dispositivos.',
  'protocolo_indicado': "Protocolo de Terapia de Sonido y Grounding para Alineación del Campo (ref. Oschman 'Energy "
                        "Medicine'; Goldman 'Healing Sounds'; Chevalier et al. 'Earthing' Journal of Environmental and "
                        'Public Health 2012). Intervención 1 — Earthing / Grounding: caminar descalzo sobre tierra, '
                        'hierba o playa 20-30 minutos diarios. La tierra tiene una carga negativa constante; al '
                        'establecer contacto físico, los electrones libres se transfieren al cuerpo. El estudio de '
                        'Chevalier et al. (2012) muestra mejora de la HRV con grounding. Intervención 2 — Frecuencia '
                        'Schumann (7.83 Hz): meditaciones con binaural beats a 7.83 Hz (diferencia de frecuencia entre '
                        'ambos oídos) para sincronizar el cerebro con la frecuencia terrestre (disponibles en '
                        'plataformas de audio). Intervención 3 — Higiene electromagnética: modo avión nocturno en el '
                        'teléfono o alejarlo de la cama al menos 1.5m; apagar el router por las noches; reducir '
                        'exposición a pantallas 1-2h antes de dormir. Intervención 4 — Terapia de sonido: cuencos de '
                        "cuarzo sintonizados a 174 Hz (nota F en escala Solfeggio: 'la frecuencia de la Tierra') "
                        'tienen efecto de re-sincronización. Sesión de 45-60 minutos.',
  'contraindicaciones': 'No prescribir como único tratamiento síntomas neurológicos (cefalea, tinnitus, vértigo) sin '
                        'descarte médico previo. El grounding descalzo no está indicado en personas con diabetes '
                        '(neuropatía periférica) o con heridas en los pies. Los binaural beats no están indicados en '
                        'personas con epilepsia.',
  'integracion': 'PSI-PNI: la interrupción del sueño por dispositivos tiene correlato directo en el cortisol nocturno '
                 'y la supresión de melatonina — la higiene del sueño es parte central del protocolo de PNI. AYU-YOG: '
                 'el pranayama matutino al aire libre combina respiración consciente con exposición a la frecuencia '
                 'Schumann natural. BIO-ALO: si los síntomas incluyen tinnitus persistente, el otorrino debe descartar '
                 'causas orgánicas antes de atribuirlo a desalineación electromagnética.'},
 {'id': 'D23',
  'titulo': 'Patrón de Resignación Aprendida',
  'descripcion': 'Programación profunda de que el cambio es imposible, generando pasividad ante el sufrimiento y '
                 'dificultad para buscar ayuda.',
  'marco_asociado': 'Socio-familiar (Contexto y Sistemas)',
  'tecnica_asociada': 'SOC-GEN',
  'sintomas': ['pasividad',
               "frase 'así soy'",
               'dificultad para pedir ayuda',
               'crónica de quejas sin acción',
               'identificación con el sufrimiento'],
  'etiologia': "La resignación aprendida (Seligman, 'Helplessness', 1975) surge cuando el individuo experimenta "
               'repetidamente que sus acciones no producen cambios en los resultados adversos: el control es inútil. '
               "Esta experiencia se generaliza: 'nada de lo que haga cambia nada'. El origen puede ser personal "
               '(infancia con impotencia real), familiar (sistema familiar donde la queja es la única comunicación), o '
               'cultural (comunidades con historia de opresión sostenida).',
  'mecanismo': 'Seligman demostró experimentalmente que animales expuestos a shocks inescapables no intentaban escapar '
               'cuando el shock se volvía escapable: el patrón neural de indefensión se había instalado. El correlato '
               'neurobiológico en humanos es una hipoactivación del circuito prefrontal-estriado de motivación y '
               'recompensa (déficit dopaminérgico en el núcleo accumbens) y una hiperactivación del eje HPA. La '
               "terapia narrativa de White y Epston propone que el patrón no es una 'deficiencia personal' sino una "
               "historia que puede ser re-escrita (ref. White & Epston 'Narrative Means to Therapeutic Ends').",
  'patron_diagnostico': "Evaluación clínica: historia de intentos fallidos de cambio, sensación de que 'así es la "
                        "vida' o 'yo soy así', pasividad ante el sufrimiento, dificultad para generar metas o "
                        'visualizar un futuro diferente. Escala de Desesperanza de Beck (BHS). Distinguir de depresión '
                        'mayor (pueden coexistir): en la resignación aprendida el afecto puede estar relativamente '
                        'preservado, pero la iniciativa está abolida. Historia familiar: ¿era la queja sin acción el '
                        'patrón de comunicación familiar?',
  'protocolo_indicado': 'Protocolo de Terapia Narrativa y Genograma para Resignación Aprendida (ref. White & Epston '
                        "'Narrative Means to Therapeutic Ends'; Seligman 'Learned Optimism'; McGoldrick 'Genograms'). "
                        'Fase 1 — Externalización del problema (White & Epston): el problema no es el paciente, sino '
                        "una historia que el paciente porta. Dar nombre a la historia: '¿Cómo llamarías a esa voz que "
                        "te dice que nada puede cambiar? ¿El Resignado, El Muro...?' Esto crea distancia entre el "
                        "paciente y el patrón. Fase 2 — Búsqueda de excepciones ('unique outcomes'): el terapeuta "
                        "busca activamente momentos en que el paciente SÍ actuó a pesar de la resignación. '¿Hubo "
                        "alguna vez que intentaste algo diferente aunque no sabías si resultaría?' Cada excepción es "
                        'una prueba contra la historia dominante. Fase 3 — Construcción de la historia alternativa: a '
                        "partir de las excepciones, construir una narrativa alternativa: 'Eres alguien que a veces, "
                        "contra todo pronóstico, actúa'. La nueva narrativa se ancla en acciones concretas pequeñas. "
                        'Fase 4 — Genograma de resiliencia: en lugar de solo buscar patrones negativos, buscar en el '
                        'árbol familiar qué ancestros resistieron, sobrevivieron, se reinventaron. La resiliencia '
                        'familiar también se transmite.',
  'contraindicaciones': 'No confundir resignación aprendida con depresión mayor: si hay ideación suicida o incapacidad '
                        'funcional severa, el manejo psiquiátrico es prioritario. No aplicar la terapia narrativa como '
                        "'positivismo forzado': la validación del dolor y de los intentos fallidos del pasado es el "
                        'primer paso. No iniciar el trabajo de excepciones antes de que el paciente sienta que su '
                        'sufrimiento fue comprendido.',
  'integracion': 'PSI-PNI: la resignación aprendida tiene sustrato neurobiológico en el déficit dopaminérgico y en la '
                 'disregulación del eje HPA — el ejercicio aeróbico regular (que aumenta la dopamina y el BDNF) es una '
                 "intervención biológica complementaria. PSI-BIO: el patrón de 'no poder' puede tener raíz en un "
                 'conflicto biológico de desvalorización (D09) o de territorio (D20). VIB-RES: el trabajo de Resonance '
                 'Repatterning puede ayudar a desanclar la frecuencia de resignación del sistema nervioso.'},
 {'id': 'D24',
  'titulo': 'Síndrome de Deficiencia Inmunitaria Funcional',
  'descripcion': 'Debilitamiento adquirido de la respuesta inmune por la acción combinada y sostenida de estrés '
                 'crónico, deficiencias nutricionales específicas, sueño insuficiente y disbiosis intestinal. No es '
                 'una inmunodeficiencia primaria ni secundaria clásica, sino una desregulación funcional reversible '
                 'con el abordaje correcto.',
  'marco_asociado': 'Biomédico (Occidental)',
  'tecnica_asociada': 'BIO-ALO',
  'sintomas': ['infecciones recurrentes',
               'cicatrización lenta',
               'fatiga persistente',
               'herpes recurrente',
               'alergias múltiples'],
  'etiologia': 'La inmunosupresión funcional resulta de la convergencia de: estrés crónico (el cortisol elevado '
               'suprime los linfocitos T y la producción de citocinas Th1), deficiencias de zinc, vitamina D, vitamina '
               'C y selenio (micronutrientes esenciales para la maduración y función de células inmunes), sueño '
               'insuficiente (<7h por noche reduce las células NK hasta un 70% tras una sola noche) y disbiosis '
               'intestinal (el 70% del tejido linfoide asociado a mucosas está en el intestino).',
  'mecanismo': 'El cortisol crónico suprime la inmunidad celular (linfocitos T CD4 y CD8, células NK) mientras '
               'mantiene activa la inmunidad humoral de tipo Th2, generando un desbalance Th1/Th2 que explica la mayor '
               'susceptibilidad a virus y bacterias intracelulares, y la aparición de alergias. La deficiencia de zinc '
               'deteriora la diferenciación tímica de linfocitos T y reduce la producción de interferón-gamma. La '
               'disbiosis reduce la IgA secretora intestinal, la primera línea de defensa mucosa.',
  'patron_diagnostico': 'Hemograma completo con fórmula leucocitaria (linfocitos, neutrófilos, monocitos). '
                        'Inmunoglobulinas (IgA, IgM, IgG). Vitamina D (25-OH; nivel óptimo >40 ng/mL), zinc sérico, '
                        'ferritina, PCR ultrasensible. Cortisol en saliva en 4 puntos del día (ritmo circadiano del '
                        'cortisol como marcador de disregulación HPA). Es imprescindible descartar VIH, neoplasia '
                        'hematológica y diabetes no controlada antes de concluir que es funcional.',
  'protocolo_indicado': 'Corrección de deficiencias: zinc 15-30mg/día, vitamina D3 2000-5000 UI/día con K2, vitamina C '
                        '500mg-1g/día, selenio 100-200mcg/día. Higiene del sueño: 7-8h mínimo, oscuridad total, sin '
                        'pantallas 1h antes (la luz azul suprime melatonina e inmunomodulación nocturna). Adaptógenos '
                        'con evidencia: Ashwagandha (KSM-66, 600mg/día), beta-glucanos de hongo reishi o shiitake. '
                        'Gestión del cortisol: intervención en estrés crónico es tan importante como la '
                        'suplementación.',
  'contraindicaciones': 'No iniciar inmunoestimuladores (Echinacea, beta-glucanos) en personas con enfermedades '
                        'autoinmunes activas (artritis reumatoide, lupus, esclerosis múltiple): pueden exacerbar la '
                        'inflamación autoinmune. No mantener zinc >40mg/día por más de 4 semanas sin supervisión: '
                        'compite con la absorción de cobre y puede generar deficiencia de cobre.',
  'integracion': 'PSI-PNI: el eje estrés-inmunidad es tan determinante que sin gestión del estrés el protocolo '
                 'nutricional es insuficiente. BIO-NUT: la suplementación específica es la base del protocolo. AYU: '
                 'correlaciona con disminución de Ojas (vitalidad profunda) y desequilibrio de Kapha; el Panchakarma '
                 'puede complementar la fase de reparación.'},
 {'id': 'D25',
  'titulo': 'Bloqueo del Flujo Pránico',
  'descripcion': 'Obstrucción del flujo de prana (energía vital) por estancamiento emocional, generando fatiga, '
                 'opresión y desconexión corporal.',
  'marco_asociado': 'Ayurveda',
  'tecnica_asociada': 'AYU-YOG',
  'sintomas': ['fatiga sin causa',
               'opresión torácica',
               'respiración superficial',
               'desconexión corporal',
               "sensación de estar 'apagado'"],
  'etiologia': 'El Prana (fuerza vital, análogo al Qi chino) circula por los Nadis (canales energéticos sutiles). El '
               'bloqueo del flujo pránico ocurre cuando: las emociones no expresadas obstruyen los nadis (como una '
               'represa), el sistema nervioso está en exceso de activación simpática (Prana perturbado activa el '
               'Vata), la respiración es crónicamente superficial, y los chakras (centros energéticos donde los nadis '
               "se entrecruzan) están en desequilibrio (ref. Frawley 'Yoga and Ayurveda', cap. 6-7).",
  'mecanismo': 'En el modelo ayurvédico, el Prana Vayu (subdivisión del Prana que gobierna la entrada de la '
               "respiración y la recepción) cuando está bloqueado impide 'recibir' energía. El Udana Vayu (prana que "
               'asciende) bloquea la expresión de la voz y el entusiasmo. El Samana Vayu (prana del centro, digestión) '
               'bloquea la integración de experiencias cuando está perturbado. El Yoga y el Pranayama son las '
               'herramientas principales de Ayurveda para restaurar el flujo pránico.',
  'patron_diagnostico': 'Evaluación ayurvédica: observar la respiración espontánea del consultante (¿es superficial, '
                        'irregular, contenida en el pecho?). Tensión en la musculatura respiratoria accesoria '
                        "(esternocleidomastoideo, escalenos). Pregunta directa: '¿Sientes que tu energía fluye "
                        "libremente o que hay zonas donde se atasca?' Localización del bloqueo: el consultante señala "
                        "la zona más 'muerta' o 'apagada' del cuerpo.",
  'protocolo_indicado': "Protocolo de Yoga y Pranayama para Bloqueo del Flujo Pránico (ref. Frawley 'Yoga and "
                        "Ayurveda', cap. 6-7; Lad 'Textbook of Ayurveda Vol.2'). Progresión pranayama por semanas: "
                        'Semana 1-2 — Respiración abdominal consciente (Diaphragmatic breathing): 5 min mañana y '
                        'noche. Mano derecha en el pecho, mano izquierda en el abdomen. Inhalar 4s (el abdomen sube), '
                        'sostener 2s, exhalar 6s (el abdomen baja). Restaura el patrón natural de respiración. Semana '
                        '3-4 — Nadi Shodhana (Respiración Alternada): el pranayama más importante para limpiar los '
                        'nadis. Técnica: tapar el orificio nasal derecho con el pulgar, inhalar por el izquierdo (4 '
                        'tiempos); tapar ambos, sostener (4 tiempos); tapar el izquierdo con el anular, exhalar por el '
                        'derecho (8 tiempos). Invertir. 5-10 minutos diarios. Semana 5 en adelante — Bhramari '
                        '(respiración abeja): inhalar profundo, exhalar con sonido mmmmm. El sonido genera vibración '
                        'en el cráneo y el tórax que libera bloqueos en los chakras superiores. 10 repeticiones. Yoga '
                        'específico: posturas de apertura del pecho (Bhujangasana — cobra, Ustrasana — camello, '
                        'Matsyasana — pez) para abrir el chakra cardíaco y el canal central (Sushumna Nadi). Posturas '
                        'de torsión para liberar el Samana Vayu. Savasana al final con visualización del prana '
                        'fluyendo libremente. Nasya: aceite de sésamo en las fosas nasales (3-5 gotas en cada narina) '
                        'al despertar activa el flujo pránico cerebral.',
  'contraindicaciones': 'Nadi Shodhana y Bhastrika contraindicados en pacientes hipertensos severos, cardíacos '
                        'descompensados, o con patología respiratoria aguda. No enseñar Pranayama avanzado (retención '
                        'larga, Kumbhaka) sin supervisión de un instructor de yoga con formación terapéutica. Las '
                        'posturas de apertura del pecho están contraindicadas en personas con protrusión discal '
                        'cervical severa.',
  'integracion': 'MTC-ACU: el bloqueo del flujo pránico tiene correlato en el Estancamiento de Qi de Hígado (D01) o en '
                 'la Deficiencia de Qi de Bazo (D06) — el Prana del Ayurveda y el Qi de la MTC son conceptos análogos '
                 'aunque no idénticos. PSI-SOM: la respiración superficial es el marcador somático del SNA en modo de '
                 'alarma — el Somatic Experiencing y el trabajo de respiración del yoga se complementan. BIO-FIS: la '
                 'fisioterapia respiratoria (reeducación de patrones respiratorios) es el correlato biomédico del '
                 'trabajo pránico — pueden trabajarse en paralelo.'},
 {'id': 'D27',
  'titulo': 'Congestión Refleja Sistémica',
  'descripcion': 'Patrón de tensión acumulada y bloqueo circulatorio que afecta múltiples órganos y sistemas '
                 'simultáneamente, detectable y tratable a través del mapa reflejo del pie y la mano.',
  'marco_asociado': 'Biomédico (Occidental)',
  'tecnica_asociada': 'BIO-REF',
  'sintomas': ['sensibilidad en zonas reflejas del pie',
               'fatiga sistémica',
               'tensión sin localización precisa',
               'digestión lenta',
               'circulación deficiente en extremidades',
               'tensión en hombros y cuello'],
  'etiologia': 'La congestión refleja sistémica resulta de la acumulación de tensión en tejidos conectivos que '
               'corresponden, según los mapas de zona de Fitzgerald (1917) e Ingham (1938), a órganos y sistemas '
               'específicos. La teoría de zonas postula que el cuerpo está organizado en 10 zonas longitudinales (5 '
               'por cada lado), y que la presión en los puntos reflejo del pie o la mano envía impulsos nerviosos al '
               'órgano correspondiente, facilitando la liberación de la tensión y mejorando la circulación local.',
  'mecanismo': 'La reflexología actúa a través de múltiples mecanismos: (1) estimulación de terminaciones nerviosas '
               '(el pie tiene más de 7,000 terminaciones nerviosas), (2) liberación de endorfinas y reducción del '
               'cortisol por el efecto de la presión táctil, (3) mejora de la microcirculación local y sistémica, (4) '
               "efecto de relajación del sistema nervioso autónomo. Los estudios de Kunz & Kunz ('Complete Reflexology "
               "for Life') y Dougans ('The Complete Illustrated Guide to Reflexology') documentan mejoras en "
               'circulación periférica, reducción del dolor y mejora de la función de órganos en pacientes tratados '
               'con reflexología.',
  'patron_diagnostico': 'Exploración reflexológica del pie: el terapeuta palpa sistemáticamente las zonas reflejas '
                        'buscando: sensibilidad dolorosa o exquisita al tacto, granulaciones o cristalizaciones en el '
                        'tejido subcutáneo, cambios de temperatura local, tensión muscular aumentada. Zonas '
                        'frecuentemente reactivas: zona lumbar (borde interno del pie, arco plantar bajo); zona '
                        'digestiva (centro del arco plantar); zona hombros/cuello (base de los dedos y almohadilla '
                        'metatarsal); zona renal/suprarrenal (arco plantar medio). La sensibilidad en una zona refleja '
                        'no es diagnóstico pero orienta sobre los sistemas que requieren más atención.',
  'protocolo_indicado': "Protocolo de Reflexología para Congestión Sistémica (ref. Ingham 'Stories the Feet Can Tell'; "
                        "Dougans 'The Complete Illustrated Guide to Reflexology'; Kunz & Kunz 'Complete Reflexology "
                        "for Life'). Sesión completa (50-60 min): el paciente en posición semirrecostada, pies limpios "
                        'y accesibles. El terapeuta trabaja ambos pies sistemáticamente con el pulgar (técnica del '
                        'gusano: movimiento de flexión del pulgar avanzando en pequeños pasos sobre la zona refleja). '
                        'Secuencia estándar: 1. Relajación inicial de todo el pie (amasado suave, rotación del '
                        'tobillo, 5 min). 2. Trabajo sistemático de las zonas: cabeza/cuello (dedos del pie), '
                        'tórax/pulmones (almohadilla metatarsal anterior), columna vertebral (borde interno del pie '
                        'desde el dedo gordo al talón), digestivo (arco plantar central), pelvis/zona lumbar (arco '
                        'plantar posterior y talón), sistema endocrino (puntos específicos en arco plantar). 3. Cierre '
                        'y drenaje linfático suave (5 min). Técnica de presión con pulgar (caterpillar/gusano): doblar '
                        'el pulgar en el primer nudo, avanzar en pequeños pasos de 2-3mm sobre la zona, presión '
                        'constante y sostenida (no deslizante). Zonas reactivas (muy sensibles): trabajar más despacio '
                        'con presión menor hasta que la sensibilidad disminuye en la sesión. Autoaplicación entre '
                        'sesiones: con el pulgar o un instrumento reflexológico (palo de madera o rodillo plantar), el '
                        'paciente puede trabajar las zonas más tensas 5-10 minutos diarios en el arco plantar (zona '
                        'digestiva y lumbar son las más accesibles para autoaplicación).',
  'contraindicaciones': 'No aplicar reflexología en: trombosis venosa profunda activa (el estímulo circulatorio puede '
                        'movilizar un coágulo), fracturas o lesiones agudas en los pies, infecciones locales activas '
                        '(hongos, verrugas, heridas abiertas en el pie), primer trimestre de embarazo (precaución con '
                        'puntos uterinos y pélvicos). Precaución en diabetes con neuropatía periférica (reducir la '
                        'presión).',
  'integracion': 'BIO-FIS: la reflexología puede preceder a la sesión de fisioterapia para reducir el tono muscular '
                 'general y mejorar la receptividad al tratamiento manual. MTC-AUR: auriculoterapia y reflexología son '
                 'técnicas de microsistema complementarias — ambas trabajan un mapa del cuerpo completo en una zona '
                 'pequeña. MTC-ACU: los puntos reflejos del pie tienen correlatos con los puntos de acupuntura Jing '
                 'Well (puntos extremos de los meridianos en los dedos del pie) — pueden estimularse en conjunto.'}]
