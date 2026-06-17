"""
Servicio del I Ching (El Libro de las Mutaciones — Enfoque Taoísta).

Implementa el método clásico de las 3 monedas para generar hexagramas.
Cada línea se determina por la suma de 3 monedas:
- 6 (3 cruces) = Yin móvil (cambia a Yang)
- 7 (2 cruces, 1 cara) = Yang estable
- 8 (2 caras, 1 cruz) = Yin estable
- 9 (3 caras) = Yang móvil (cambia a Yin)
"""

import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════
# CATÁLOGO DE LOS 64 HEXAGRAMAS DEL I CHING
# ═══════════════════════════════════════════════════

HEXAGRAMAS = {
    1:  {"nombre": "乾 — El Creador", "dictamen": "El Creador obra sublime éxito, perseverando.", "imagen": "El cielo arriba, el cielo abajo. El ser superior se fortalece sin cesar."},
    2:  {"nombre": "坤 — Lo Receptivo", "dictamen": "Lo Receptivo trae sublime éxito a través de la yegua salvaje.", "imagen": "La tierra abajo, la tierra arriba. El ser superior sostiene el mundo con virtud."},
    3:  {"nombre": "屯 — Dificultad Inicial", "dictamen": "Dificultad inicial obra sublime éxito, perseverando.", "imagen": "Nubes y trueno. El ser superior pone orden en el caos."},
    4:  {"nombre": "蒙 — Juventud y Locura", "dictamen": "La juventud ha encontrado al maestro. No busco al joven, el joven me busca.", "imagen": "Un manantial brota al pie de la montaña. El ser superior cultiva su carácter."},
    5:  {"nombre": "需 — Espera", "dictamen": " Espera con sinceridad trae luz brillante y éxito.", "imagen": "Nubes ascienden al cielo. El ser superior come, bebe y se alegra."},
    6:  {"nombre": "訟 — Conflicto", "dictamen": "Conflicto: eres sincero pero hay obstáculo. La prudencia trae buena fortuna.", "imagen": "Cielo y agua van por caminos opuestos. El ser superior planifica con cuidado."},
    7:  {"nombre": "師 — El Ejército", "dictamen": "El ejército necesita perseverancia y un hombre fuerte. Buena fortuna sin culpa.", "imagen": "Agua en la tierra. El ser superior aumenta sus fuerzas con generosidad."},
    8:  {"nombre": "比 — Unión", "dictamen": "Unión trae buena fortuna. Los que dudan aún pueden unirse al final.", "imagen": "Agua sobre la tierra. Los reyes antiguos establecían estados y mantenían lazos."},
    9:  {"nombre": "小畜 — Pequeño Poder", "dictamen": "El pequeño poder: éxito denso. Nubes densas, no hay lluvia de nuestra región.", "imagen": "Viento sopla en el cielo. El ser superior refina su apariencia."},
    10: {"nombre": "履 — Caminar con Cuidado", "dictamen": "Caminar sobre la cola del tigre. No muerde. Éxito.", "imagen": "Cielo arriba, lago abajo. El ser superior discrimina entre lo alto y lo bajo."},
    11: {"nombre": "泰 — La Paz", "dictamen": "La Paz: lo pequeño se va, lo grande viene. Buena fortuna, éxito.", "imagen": "Cielo y tierra se unen. El gobernante apoya el camino del cielo y la tierra."},
    12: {"nombre": "否 — El Estancamiento", "dictamen": "El estancamiento: lo grande se va, lo pequeño viene.", "imagen": "Cielo y tierra no se comunican. El ser superior se retira a su interior."},
    13: {"nombre": "同人 — Comunidad", "dictamen": "Comunidad en el campo. Éxito. Es beneficioso cruzar las grandes aguas.", "imagen": "Cielo junto con fuego. El ser superior organiza clanes y distingue las cosas."},
    14: {"nombre": "大有 — Gran Posesión", "dictamen": "Gran posesión: supremo éxito.", "imagen": "Fuego en el cielo. El ser superior fomenta lo bueno y rechaza lo malo."},
    15: {"nombre": "謙 — Modestia", "dictamen": "Modestia: éxito. El ser superior lleva la carga.", "imagen": "Montaña dentro de la tierra. El ser superior reduce lo mucho y aumenta lo poco."},
    16: {"nombre": "豫 — Entusiasmo", "dictamen": "Entusiasmo: es beneficioso instalar ayudantes y poner ejércitos en marcha.", "imagen": "Trueno resuena sobre la tierra. El antiguo rey compuso música para honrar la virtud."},
    17: {"nombre": "隨 — Seguir", "dictamen": "Seguir: sublime éxito, perseverando. Sin culpa.", "imagen": "Trueno en el centro del lago. El ser superior descansa cuando llega la noche."},
    18: {"nombre": "蠱 — Trabajo en lo Deteriorado", "dictamen": "Trabajo en lo deteriorado: sublime éxito. Es beneficioso cruzar las grandes aguas.", "imagen": "Viento sopla al pie de la montaña. El ser superior agita al pueblo y fortalece su espíritu."},
    19: {"nombre": "臨 — Aproximación", "dictamen": "Aproximación: sublime éxito, perseverando.", "imagen": "Tierra sobre el lago. El ser superior es inagotable en su enseñanza y protección."},
    20: {"nombre": "觀 — Contemplación", "dictamen": "Contemplación: se ha ofrecido el lavatorio pero no la ofrenda.", "imagen": "Viento sopla sobre la tierra. Los reyes antiguos visitaban las cuatro direcciones."},
    21: {"nombre": "噬嗑 — Morder a Través", "dictamen": "Morder a través: éxito. Es beneficioso administrar justicia.", "imagen": "Trueno y relámpago. Los reyes antiguos establecieron leyes con claridad."},
    22: {"nombre": "賁 — Gracia", "dictamen": "Gracia: éxito. En asuntos pequeños es beneficioso emprender.", "imagen": "Fuego al pie de la montaña. El ser superior ilumina los asuntos con claridad."},
    23: {"nombre": "剝 — Desintegración", "dictamen": "Desintegración: no es beneficioso emprender nada.", "imagen": "Montaña apoyada en la tierra. Los superiores aseguran su posición dando a los inferiores."},
    24: {"nombre": "復 — Retorno", "dictamen": "Retorno: éxito. Los amigos vienen sin culpa.", "imagen": "Trueno dentro de la tierra. Los reyes antiguos cerraban los pasos en el solsticio."},
    25: {"nombre": "無妄 — Inocencia", "dictamen": "Inocencia: sublime éxito, perseverando.", "imagen": "Trueno rueda bajo el cielo. Todas las cosas alcanzan el estado natural de inocencia."},
    26: {"nombre": "大畜 — Gran Acumulación", "dictamen": "Gran acumulación: perseverancia. No comer en casa trae buena fortuna.", "imagen": "Cielo dentro de la montaña. El ser superior acumula virtud y conocimiento."},
    27: {"nombre": "頤 — Nutrición", "dictamen": "Nutrición: perseverancia trae buena fortuna. Observa la nutrición y lo que busca la boca.", "imagen": "Trueno al pie de la montaña. El ser superior es cuidadoso con sus palabras y moderado al comer."},
    28: {"nombre": "大過 — Gran Exceso", "dictamen": "Gran exceso: el tejado se inclina. Es beneficioso tener a dónde ir. Éxito.", "imagen": "El lago sumerge los árboles. El ser superior se sostiene solo sin temor."},
    29: {"nombre": "坎 — El Abismal", "dictamen": "El abismal: si eres sincero, tienes éxito en tu corazón.", "imagen": "Agua fluye sin cesar. El ser superior camina en virtud constante."},
    30: {"nombre": "離 — Lo Adherente", "dictamen": "Lo adherente: perseverancia trae éxito. Cuida la vaca, buena fortuna.", "imagen": "Lo que brilla se eleva. El ser superior brilla con virtud resplandeciente."},
    31: {"nombre": "咸 — Influencia", "dictamen": "Influencia: éxito. Perseverar trae buena fortuna. Tomar una doncella trae buena fortuna.", "imagen": "Lago sobre la montaña. El ser superior recibe a los demás con vacuidad."},
    32: {"nombre": "恆 — Duración", "dictamen": "Duración: éxito. Sin culpa. Perseverancia trae buena fortuna.", "imagen": "Trueno y viento. El ser superior se mantiene firme y no cambia de dirección."},
    33: {"nombre": "遁 — Retirada", "dictamen": "Retirada: éxito. En lo pequeño, perseverancia trae buena fortuna.", "imagen": "Montaña bajo el cielo. El ser superior mantiene distancia de los inferiores."},
    34: {"nombre": "大壯 — Gran Poder", "dictamen": "Gran poder: perseverancia trae buena fortuna.", "imagen": "Trueno en el cielo. El ser superior no pisa caminos que no estén de acuerdo con el orden."},
    35: {"nombre": "晉 — Progreso", "dictamen": "Progreso: el poderoso príncipe es honrado con caballos en gran número.", "imagen": "El sol se eleva sobre la tierra. El ser superior brilla con su propia luz."},
    36: {"nombre": "明夷 — Oscurecimiento de la Luz", "dictamen": "Oscurecimiento de la luz: en la adversidad es beneficioso perseverar.", "imagen": "La luz ha penetrado en la tierra. El ser superior vela su brillo en medio de la multitud."},
    37: {"nombre": "家人 — La Familia", "dictamen": "La familia: perseverancia de la mujer trae buena fortuna.", "imagen": "Fuego sale del viento. El ser superior tiene sustancia en sus palabras y duración en su modo de vivir."},
    38: {"nombre": "睽 — Oposición", "dictamen": "Oposición: en asuntos pequeños, buena fortuna.", "imagen": "Fuego arriba, lago abajo. El ser conserva su individualidad en la comunidad."},
    39: {"nombre": "蹇 — Obstrucción", "dictamen": "Obstrucción: el oeste y el sur traen buena fortuna. El norte y el este traen desgracia.", "imagen": "Agua en la montaña. El ser superior dirige su atención a sí mismo y moldea su carácter."},
    40: {"nombre": "解 — Liberación", "dictamen": "Liberación: el oeste y el sur traen buena fortuna.", "imagen": "Trueno y lluvia se liberan. El ser superior perdona los errores y absuelve las faltas."},
    41: {"nombre": "損 — Disminución", "dictamen": "Disminución combinada con sinceridad trae supremo éxito.", "imagen": "Lago al pie de la montaña. El ser superior controla la ira y refrena los instintos."},
    42: {"nombre": "益 — Aumento", "dictamen": "Aumento: es beneficioso emprender algo. Es beneficioso cruzar las grandes aguas.", "imagen": "Viento y trueno. El ser superior, al ver lo bueno, lo imita; al tener defectos, se corrige."},
    43: {"nombre": "夬 — Resolución", "dictamen": "Resolución: se proclama la verdad en la corte del rey.", "imagen": "Lago ha subido al cielo. El ser superior dispensa riqueza hacia abajo y se abstiene de descansar en su virtud."},
    44: {"nombre": "姤 — Encuentro", "dictamen": "Encuentro: la doncella es poderosa. No tomar tal doncella.", "imagen": "Bajo el cielo, viento. El príncipe anuncia sus órdenes a las cuatro direcciones."},
    45: {"nombre": "萃 — Reunión", "dictamen": "Reunión: éxito. El rey se acerca a su templo.", "imagen": "Lago sobre la tierra. El ser superior renueva sus armas para lo inesperado."},
    46: {"nombre": "升 — Ascenso", "dictamen": "Ascenso: gran éxito. Se debe ver al gran hombre.", "imagen": "Árbol dentro de la tierra. El ser superior acumula lo pequeño para alcanzar lo grande."},
    47: {"nombre": "困 — Agotamiento", "dictamen": "Agotamiento: éxito. Perseverancia. El gran hombre trae buena fortuna.", "imagen": "No hay agua en el lago. El arriesga su vida para cumplir su voluntad."},
    48: {"nombre": "井 — El Pozo", "dictamen": "El pozo: la ciudad puede cambiar pero el pozo no.", "imagen": "Agua sobre la madera. El ser superior anima al pueblo en su trabajo y los exhorta a ayudarse mutuamente."},
    49: {"nombre": "革 — Revolución", "dictamen": "Revolución: en tu día eres creído. Sublime éxito.", "imagen": "Fuego en el lago. El ser superior pone en orden los tiempos y aclara las estaciones."},
    50: {"nombre": "鼎 — El Caldero", "dictamen": "El caldero: supremo éxito, buena fortuna.", "imagen": "Fuego sobre madera. El ser superior consolida su destino haciendo que su posición sea correcta."},
    51: {"nombre": "震 — Trueno", "dictamen": "Trueno: éxito. Trueno viene, ¡ja, ja! Luego viene la calma.", "imagen": "Trueno repetido. El ser superior pone su vida en orden por medio del temor."},
    52: {"nombre": "艮 — Quietud", "dictamen": "Quietud: quietud en la espalda. No sientes tu cuerpo.", "imagen": "Montañas de pie juntas. El ser superior no piensa más allá de su situación."},
    53: {"nombre": "漸 — Desarrollo Gradual", "dictamen": "Desarrollo gradual: la doncella que se casa trae buena fortuna.", "imagen": "Árbol sobre la montaña. El ser superior se sostiene en la dignidad y la virtud."},
    54: {"nombre": "歸妹 — La Doncella que se Casa", "dictamen": "La doncella que se casa: emprender trae desgracia.", "imagen": "Trueno sobre el lago. El ser superior entiende lo transitorio a la luz del eterno."},
    55: {"nombre": "豐 — Abundancia", "dictamen": "Abundancia: éxito. El rey alcanza la abundancia.", "imagen": "Trueno y relámpago llegan juntos. El ser superior decide los litigios y ejecuta los castigos."},
    56: {"nombre": "旅 — El Viajero", "dictamen": "El viajero: éxito a través de lo pequeño. Perseverancia trae buena fortuna.", "imagen": "Fuego en la montaña. El ser superior es claro y cauteloso al imponer penas."},
    57: {"nombre": "巽 — Lo Suave", "dictamen": "Lo suave: éxito a través de lo pequeño.", "imagen": "Viento que sigue al viento. El ser superior extiende sus órdenes al exterior."},
    58: {"nombre": "兌 — La Alegría", "dictamen": "La alegría: éxito. Perseverancia es favorable.", "imagen": "Lagos descansando uno sobre otro. El ser superior se reúne con amigos para discutir y practicar."},
    59: {"nombre": "渙 — Dispersión", "dictamen": "Dispersión: éxito. El rey se acerca a su templo.", "imagen": "Viento sopla sobre el agua. Los reyes antiguos sacrificaron al Señor y construyeron templos."},
    60: {"nombre": "節 — Limitación", "dictamen": "Limitación: éxito. La limitación amarga no debe perseverarse.", "imagen": "Agua sobre el lago. El ser superior crea número y medida y examina la virtud y la conducta."},
    61: {"nombre": "中孚 — Verdad Interior", "dictamen": "Verdad interior: los cerdos y los peces traen buena fortuna.", "imagen": "Viento sobre el lago. El ser superior discute los asuntos criminales y aplaza las ejecuciones."},
    62: {"nombre": "小過 — Pequeño Exceso", "dictamen": "Pequeño exceso: éxito. Perseverancia es favorable para asuntos pequeños.", "imagen": "Trueno en la montaña. El ser superior en su conducta excede en respeto."},
    63: {"nombre": "既濟 — Después de la Consumación", "dictamen": "Después de la consumación: éxito en lo pequeño. Perseverancia trae buena fortuna.", "imagen": "Agua sobre el fuego. El ser superior piensa en la desgracia y la previene de antemano."},
    64: {"nombre": "未濟 — Antes de la Consumación", "dictamen": "Antes de la consumación: éxito. Pero la zorra moja su cola al cruzar el río.", "imagen": "Fuego sobre el agua. El ser superior es cuidadoso al distinguir las cosas y cada una en su lugar."},
}

# Fallback por posición de línea (cuando no hay texto específico)
FALLBACK_LINEA = {
    1: "En el inicio, el movimiento surge del fundamento. Algo que parecía dormido despierta.",
    2: "En el segundo lugar, la energía se acumula en silencio. Lo que madura aquí tiene raíces.",
    3: "En el umbral entre interior y exterior, la tensión es creativa. Actúa con conciencia.",
    4: "Cerca del lugar del gobernante, la cautela y el discernimiento son la llave.",
    5: "En la posición central superior, lo que se transforma irradia hacia el conjunto.",
    6: "En el extremo, el ciclo completa su arco. Lo que termina aquí abre espacio.",
}

TEXTOS_LINEAS_MOVILES = {
    1:  {1: "Dragón oculto. No actúes.", 2: "Dragón en el campo. Beneficioso ver al gran hombre.", 3: "Activo todo el día; alerta por la noche. Perseverancia, sin culpa.", 4: "Salto en el abismo. Sin culpa.", 5: "Dragón volador en el cielo. Beneficioso ver al gran hombre.", 6: "Dragón arrogante: habrá arrepentimiento."},
    2:  {1: "Escarcha bajo los pies. El hielo firme llega pronto.", 2: "Recto, cuadrado, grande. Sin propósito, nada desfavorable.", 3: "Oculta tu virtud. Persevera. Al servir, no busques resultados.", 4: "Un saco atado. Sin culpa, sin elogio.", 5: "Vestido amarillo: suprema buena fortuna.", 6: "Dragones luchan en el campo. Su sangre es negra y amarilla."},
    3:  {1: "Vacilación y dificultad al inicio. Beneficioso nombrar ayudantes.", 2: "La doncella es fiel. Diez años pasan. Al fin, unión.", 3: "Avanzar sin guía en el bosque. Mejor detenerse.", 4: "El carruaje se detiene. Busca compañía para proseguir.", 5: "Dificultad en la gracia. Un poco de perseverancia trae buena fortuna.", 6: "Caballos y carruaje se separan. Lágrimas."},
    4:  {1: "La locura necesita disciplina. Sin culpa.", 2: "Soportar al necio con bondad es buena fortuna.", 3: "No tomes a quien no se posee a sí mismo. Sin beneficio.", 4: "La locura encadenada trae humillación.", 5: "La locura infantil trae buena fortuna.", 6: "Al corregir la locura, no excedas. Defiéndete solo de lo excesivo."},
    5:  {1: "Espera en el campo. Persevera. Sin culpa.", 2: "Espera en la arena. Hay algo de crítica. Al final, buena fortuna.", 3: "Espera en el fango. Esto trae la llegada de enemigos.", 4: "Espera en la sangre. Sal del hoyo.", 5: "Espera con vino y comida. Perseverancia trae buena fortuna.", 6: "Entramos en la cueva. Tres invitados no invitados llegan. Los honras y al final hay buena fortuna."},
    6:  {1: "No perpetúes el asunto. Hay algo de crítica. Al final, buena fortuna.", 2: "No puedes ganar el litigio. Regresa a casa. La gente de tu ciudad no será amenazada.", 3: "Alimentarte de la virtud antigua trae perseverancia y peligro, pero al final buena fortuna.", 4: "No puedes ganar el litigio. Regresa. Acepta el destino. Persevera, buena fortuna.", 5: "Litigar ante el supremo trae sublime buena fortuna.", 6: "Aun si te dan un cinturón de cuero, al final del día te lo quitarán tres veces."},
    7:  {1: "Un ejército debe salir en orden. Si no, mala fortuna acecha.", 2: "En el corazón del ejército, buena fortuna y sin culpa. El rey otorga triple recompensa.", 3: "Tal vez el ejército lleva cadáveres en el carro. Desgracia.", 4: "El ejército en retirada. Sin culpa.", 5: "Hay caza en el campo. Es beneficioso tomarla. Sin culpa. Que el de mayor edad lidere.", 6: "El gran príncipe emite órdenes. Funda estados, inviste familias. Los mediocres no deben emplearse."},
    8:  {1: "Unión sincera. Sin culpa. La sinceridad llena el recipiente. Al final llega otra buena fortuna.", 2: "Unión interior. Perseverancia trae buena fortuna.", 3: "Unión con las personas equivocadas.", 4: "Unión exterior con él. Perseverancia trae buena fortuna.", 5: "Manifestación de unión. El rey caza en tres lados. Los habitantes de delante pueden escapar. Sin advertencia.", 6: "No hay cabeza en esta unión. Desgracia."},
    9:  {1: "Retorno al propio camino. ¿Qué culpa hay en esto? Buena fortuna.", 2: "Se deja llevar al retorno. Buena fortuna.", 3: "El carro pierde las ruedas. El marido y la mujer se vuelven los ojos.", 4: "Si eres sincero, la sangre desaparece y el miedo se va. Sin culpa.", 5: "Si eres sincero y leal en la unión, enriqueces a tu vecino.", 6: "Ya ha llovido, ya ha parado. Esto se debe al carácter femenino. La mujer perseverante encuentra peligro."},
    10: {1: "Conducta simple. Progresa sin culpa.", 2: "Caminar por un camino llano y tranquilo. La perseverancia de un hombre oscuro trae buena fortuna.", 3: "Un tuerto puede ver; un cojo puede caminar. Pisará la cola del tigre. Desgracia.", 4: "Pisa la cola del tigre. Precaución y conciencia. Al final buena fortuna.", 5: "Conducta decidida. Perseverancia con conciencia del peligro.", 6: "Examina tu conducta, considera los presagios. Su retorno trae sublime buena fortuna."},
    11: {1: "Cuando se arranca una caña, viene arrastrada otra. Perseverancia trae buena fortuna.", 2: "Soporta a los incultos con benevolencia. Cruza el río con resolución.", 3: "Ninguna llanura sin pendiente. No partir sin recibir algo a cambio.", 4: "No por la riqueza propia. En medio de los vecinos, franqueza.", 5: "El soberano Yi da a su hija en matrimonio. Esto trae bendición y sublime buena fortuna.", 6: "La ciudad cae en la fosa. No uses el ejército así."},
    12: {1: "Cuando se arranca una caña, viene arrastrada otra. Perseverancia trae honor.", 2: "Soporta a los incultos. Los serviles tendrán buena fortuna.", 3: "Soporta la vergüenza.", 4: "Quien actúa por mandato supremo no comete falta. Los de igual naturaleza participan de la bendición.", 5: "El estancamiento se detiene. Grande el hombre, buena fortuna. Pero '¿y si fracasa?' así planta la morera.", 6: "El estancamiento cae primero, luego viene la alegría."},
    13: {1: "Comunidad en la puerta. Sin culpa.", 2: "Comunidad con el clan. Humillación.", 3: "Esconde armas en la maleza; sube a la colina alta. Tres años sin levantarse.", 4: "Sube a sus murallas, pero no puede atacar. Buena fortuna.", 5: "Comunidad de hombres, primero lloran, luego ríen. El gran ejército se reencuentra.", 6: "Comunidad en el campo abierto. Sin arrepentimiento."},
    14: {1: "Sin relación con lo nocivo. No hay culpa. La conciencia del peligro no trae culpa.", 2: "Gran carruaje para cargar. Tener adónde ir. Sin culpa.", 3: "Un príncipe ofrece al Hijo del Cielo. Un hombre pequeño no puede hacer esto.", 4: "Marca la diferencia con la ostentación. Sin culpa.", 5: "Su verdad se une, dignamente. Buena fortuna.", 6: "Del cielo viene la bendición. Buena fortuna. Nada que no sea beneficioso."},
    15: {1: "Un ser superior modesto puede cruzar el gran río. Buena fortuna.", 2: "La modestia se manifiesta. Perseverancia trae buena fortuna.", 3: "Un ser superior trabajador y modesto completa. Buena fortuna.", 4: "Nada que no sea beneficioso para la modestia activa.", 5: "No fanfarronear con la riqueza frente al vecino. Es beneficioso atacar con fuerza. Nada desfavorable.", 6: "La modestia se manifiesta. Beneficioso poner ejércitos en marcha para castigar la propia ciudad y el estado."},
    16: {1: "Entusiasmo que se proclama: desgracia.", 2: "Firme como una roca. No esperes al fin del día. Perseverancia trae buena fortuna.", 3: "Entusiasmo que mira hacia arriba crea arrepentimiento. Vacilación trae arrepentimiento.", 4: "La fuente del entusiasmo. Logra grandes cosas. No dudes. Los amigos se reúnen a tu alrededor.", 5: "Perseverante en la enfermedad y aun así no morir.", 6: "Entusiasmo cegado; pero si cambias después del hecho, no hay culpa."},
    17: {1: "La oficina cambia. Perseverancia trae buena fortuna. Salir por la puerta con compañía hace algo.", 2: "Si te atas al niño pierdes al hombre maduro.", 3: "Si te atas al hombre maduro pierdes al niño. Siguiendo encontrarás lo que buscas. Beneficioso permanecer perseverante.", 4: "Seguir a través del apego trae obstáculo. Perseverancia con conciencia del mal en el camino conduce a la comprensión.", 5: "Sincero en el bien. Buena fortuna.", 6: "Se está enlazado y atado. El rey hace ofrenda en la montaña del oeste."},
    18: {1: "Repara el deterioro causado por el padre. Hay un hijo; el padre difunto no tiene culpa. Peligro pero al final buena fortuna.", 2: "Repara el deterioro causado por la madre. No se puede ser demasiado perseverante.", 3: "Repara el deterioro causado por el padre. Habrá pequeño arrepentimiento. Sin gran culpa.", 4: "Tolerar el deterioro causado por el padre. Al continuar se ve la humillación.", 5: "Repara el deterioro causado por el padre. Utiliza el elogio.", 6: "No sirvas ni a reyes ni a príncipes. Establece como metas superiores tu propio ser."},
    20: {1: "Contemplación boyuna. Para el hombre común, sin culpa. Para el ser superior: humillación.", 2: "Contemplación a través de la rendija. Beneficioso para la perseverancia de la mujer.", 3: "Contemplación de mi propia vida. Decidir avanzar o retroceder.", 4: "Contemplación de la luz del reino. Es beneficioso actuar como huésped del rey.", 5: "Contemplación de mi propia vida. El ser superior está sin culpa.", 6: "Contemplar su vida. El ser superior está sin culpa."},
    24: {1: "Retorno desde una distancia corta. Sin necesidad de arrepentimiento. Sublime buena fortuna.", 2: "Quietud en el retorno. Buena fortuna.", 3: "Retorno repetido. Peligro. Sin culpa.", 4: "Caminar en el centro. Retorno solo.", 5: "Retorno noble. Sin arrepentimiento.", 6: "Extravío en el retorno. Desgracia. Se producen calamidades. Si uno pone los ejércitos en marcha, al final habrá una gran derrota."},
    29: {1: "La costumbre del abismo. Entramos en la caverna del abismo. Desgracia.", 2: "El abismo tiene riesgo. Busca lograr pequeñas cosas.", 3: "Hacia adelante y hacia atrás, peligro. Vacilación y peligro. Entrar en la caverna del abismo. No actúes.", 4: "Una jarra de vino, una escudilla de arroz. Recipientes de barro. Recibe instrucción simplemente a través de la ventana. Al final, sin culpa.", 5: "El abismo no desborda. Sólo está lleno hasta el borde. Sin culpa.", 6: "Atado con cuerdas y sogas. Encerrado en una prisión espinosa. Por tres años no encuentra el camino. Desgracia."},
    30: {1: "Pasos confusos. Pero si tomas la responsabilidad seriamente, sin culpa.", 2: "Luz amarilla. Sublime buena fortuna.", 3: "A la luz del sol poniente los hombres o cantan y golpean el cántaro o lamentan los gemidos de los viejos. Desgracia.", 4: "Su llegada es repentina. Arde, muere, es desechado.", 5: "Las lágrimas fluyen en torrentes. Hay sollozos y lamentos. Buena fortuna.", 6: "El rey lo usa para hacer una expedición. Hay gloria. Mata al jefe. Sus prisioneros no son sus propios hombres. Sin culpa."},
    36: {1: "El oscurecimiento de la luz durante el vuelo. Cuelga sus alas. El ser superior ayuna tres días en el camino. Tiene a dónde ir. El dueño le habla.", 2: "El oscurecimiento de la luz lo hiere en el muslo izquierdo. Usa el poder de un caballo para la salvación. Buena fortuna.", 3: "El oscurecimiento de la luz durante la caza hacia el sur. Captura su gran jefe. No hay que ser demasiado perseverante.", 4: "Entra en el lado izquierdo del vientre. Uno obtiene el corazón del oscurecimiento de la luz. Se deja la casa y el corral.", 5: "El oscurecimiento de la luz como en la época del príncipe Gi. Perseverancia trae buena fortuna.", 6: "No hay luz, solo oscuridad. Primero sube al cielo; luego se hunde en la tierra."},
    40: {1: "Sin culpa.", 2: "En la caza, atrapa tres zorros en el campo y recibe una flecha amarilla. Perseverancia trae buena fortuna.", 3: "Si un hombre carga algo sobre su espalda y a la vez monta a caballo, atrae a los bandidos. Perseverancia trae humillación.", 4: "Libera tu dedo del pie. El amigo viene y puede confiar en ti.", 5: "Si solo el ser superior puede liberarse: buena fortuna. Esto también prueba a los hombres inferiores.", 6: "El príncipe dispara a un halcón en el alto muro. Lo alcanza. Nada que no sea beneficioso."},
    47: {1: "Uno se sienta exhausto bajo un árbol desnudo. Entra en una sombría arboleda y no ve a nadie por tres años.", 2: "Exhausto ante el vino y la comida. Entonces viene el hombre carmesí. Es beneficioso hacer ofrenda. Emprender trae desgracia. Sin culpa.", 3: "El hombre se deja aplastar por la piedra y se apoya en zarzas y espinas. Entra en su casa y no ve a su esposa. Desgracia.", 4: "Viene muy despacio, apremiado por una carreta de oro. Humillación, pero hay un fin.", 5: "Se le corta la nariz y los pies. El hombre carmesí se queda apremiado. Pero luego viene la alegría.", 6: "Apremiado por las enredaderas trepadoras, inseguro en los movimientos. Dice: el movimiento trae arrepentimiento. Si hay arrepentimiento y se mueve, se tiene buena fortuna."},
    48: {1: "El barro del pozo no se bebe. No hay animales viejos que vengan al pozo en desuso.", 2: "En el pozo hay peces. El cántaro se rompe y escapa el agua.", 3: "El pozo se limpió pero no se bebe. Esto es tristeza de corazón porque se podría beber. Si el rey fuera lúcido, podríamos recibir su felicidad juntos.", 4: "El pozo se está reparando con ladrillo. Sin culpa.", 5: "En el pozo hay una fuente de agua clara. Se bebe de ella.", 6: "El pozo es libre. Sin cubierta. Sinceridad. Sublime buena fortuna."},
    49: {1: "Envuelto en la piel de una vaca amarilla.", 2: "Cuando tu propio día ha llegado, puedes llevar a cabo la revolución. Emprender trae buena fortuna. Sin culpa.", 3: "Emprender trae desgracia. Perseverancia es peligrosa. Cuando las conversaciones sobre la revolución han circulado tres veces, se puede confiar en ellas y uno tiene algo a lo que atenerse.", 4: "El arrepentimiento desaparece. Se confía en él. Cambia el gobierno. Buena fortuna.", 5: "El gran hombre cambia como el tigre. Antes de preguntar al oráculo, se le cree.", 6: "El ser superior cambia como un leopardo. El hombre inferior muda de cara. Emprender trae desgracia. Permanecer perseverante trae buena fortuna."},
    50: {1: "Un caldero con las patas hacia arriba. Beneficioso remover lo que está estancado. Se toma una concubina por el bien de su hijo. Sin culpa.", 2: "Hay comida en el caldero. Los compañeros de mi esposo están enfermos de envidia, pero no pueden hacerme daño. Buena fortuna.", 3: "Las asas del caldero están alteradas. Uno es obstaculizado en su manera de vivir. La grasa del faisán no se come. Cuando llueve, la culpa se disuelve. Al final, buena fortuna.", 4: "Las patas del caldero están rotas. El caldo del príncipe se vierte y su persona queda manchada. Desgracia.", 5: "El caldero tiene asas amarillas y anillas de oro. Perseverancia trae beneficio.", 6: "El caldero tiene anillas de jade. Gran buena fortuna. Nada que no sea beneficioso."},
    51: {1: "El trueno viene: jay! Luego las palabras riendo. Buena fortuna.", 2: "El trueno viene trayendo peligro. Cien mil monedas de oro perdidas. Sube las nueve colinas. No las persigas; al séptimo día las recuperarás.", 3: "El trueno viene y te deja atontado. Si el trueno te incita a actuar, no habrá culpa.", 4: "El trueno se hunde en el barro.", 5: "El trueno va y viene, peligro. Sin pérdida, pero hay cosas para hacer.", 6: "El trueno trae destrucción y terror. Mirar en derredor con ansiedad. Emprender trae desgracia. Si el trueno no llega todavía a tu propio cuerpo sino al vecino, no hay culpa."},
    52: {1: "Quietud en los dedos del pie. Sin culpa. Perseverancia continua trae buena fortuna.", 2: "Quietud en las pantorrillas. No puede rescatar a quien sigue. Su corazón está apenado.", 3: "Quietud en la cadera. La espalda se endurece. Peligro que sofoca el corazón.", 4: "Quietud en el tronco. Sin culpa.", 5: "Quietud en las mandíbulas. Las palabras tienen orden. El arrepentimiento desaparece.", 6: "Quietud sincera. Buena fortuna."},
    58: {1: "La alegría expresada mutuamente. Buena fortuna.", 2: "La alegría sincera. Buena fortuna. El arrepentimiento desaparece.", 3: "La alegría que llega. Desgracia.", 4: "La alegría que se prepara es difícil de obtener. Los que están inquietos con pensamientos limitan la alegría.", 5: "Confiar en el desintegrador es peligroso.", 6: "La alegría seductora."},
    63: {1: "Frena las ruedas. Moja la cola del zorro. Sin culpa.", 2: "La mujer pierde su velo de carro. No la busques; al séptimo día la recuperarás.", 3: "El Sublime Ancestro castigó el país demoníaco. En tres años lo venció. Los hombres corrientes no deben emplearse.", 4: "Los mejores ropajes se convierten en harapos. Ten cuidado todo el día.", 5: "El vecino del este mata un buey; esto no es tan bueno como el simple sacrificio del vecino del oeste que realmente recibe la bendición.", 6: "Se moja la cabeza. Peligro."},
    64: {1: "Moja la cola del zorro. Humillación.", 2: "Frena las ruedas. Perseverancia trae buena fortuna.", 3: "Antes de la consumación, avanzar trae desgracia. Beneficioso cruzar las grandes aguas.", 4: "Perseverancia trae buena fortuna. El arrepentimiento desaparece. El trueno golpea el país demoníaco. En tres años el gran país recibe recompensa.", 5: "Perseverancia trae buena fortuna. Sin arrepentimiento. La luz del ser superior es verdadera. Buena fortuna.", 6: "Hay confianza al beber vino. Sin culpa. Pero si uno se moja la cabeza, se pierde esto también."},
}


@dataclass
class LineaIChing:
    """Una línea del hexagrama."""
    numero: int  # 1-6 (de abajo a arriba)
    valor: int  # 6, 7, 8 o 9
    tipo: str  # "yin" o "yang"
    movil: bool  # True si es 6 o 9

    def to_dict(self) -> dict:
        return {
            "numero": self.numero,
            "valor": self.valor,
            "tipo": self.tipo,
            "movil": self.movil,
        }


@dataclass
class HexagramaIChing:
    """Hexagrama completo del I Ching."""
    numero: int
    nombre: str
    dictamen: str
    imagen: str
    lineas: list[LineaIChing] = field(default_factory=list)
    es_secundario: bool = False

    def to_dict(self) -> dict:
        return {
            "numero": self.numero,
            "nombre": self.nombre,
            "dictamen": self.dictamen,
            "imagen": self.imagen,
            "lineas": [l.to_dict() for l in self.lineas],
            "es_secundario": self.es_secundario,
        }


class IChingService:
    """
    Servicio principal del I Ching.
    Implementa el método de las 3 monedas clásico.
    """

    # Valores de las monedas: cara = 3, cruz = 2
    VALORES_MONEDAS = [2, 3]  # cruz=2, cara=3

    def lanzar_moneda(self) -> int:
        """Lanza una moneda: devuelve 2 (cruz) o 3 (cara)."""
        return random.choice(self.VALORES_MONEDAS)

    def lanzar_tres_monedas(self) -> tuple[int, int, int, int]:
        """
        Lanza 3 monedas y devuelve (moneda1, moneda2, moneda3, suma).
        Suma: 6 (3 cruces), 7 (2C+1X), 8 (2X+1C), 9 (3 caras).
        """
        m1 = self.lanzar_moneda()
        m2 = self.lanzar_moneda()
        m3 = self.lanzar_moneda()
        return m1, m2, m3, m1 + m2 + m3

    def suma_a_linea(self, suma: int) -> LineaIChing:
        """
        Convierte la suma de 3 monedas en una línea del hexagrama.
        6 = Yin móvil (---x---) → cambia a Yang
        7 = Yang estable (--------)
        8 = Yin estable (--- ---)
        9 = Yang móvil (----o----) → cambia a Yin
        """
        if suma == 6:
            return LineaIChing(numero=0, valor=6, tipo="yin", movil=True)
        elif suma == 7:
            return LineaIChing(numero=0, valor=7, tipo="yang", movil=False)
        elif suma == 8:
            return LineaIChing(numero=0, valor=8, tipo="yin", movil=False)
        elif suma == 9:
            return LineaIChing(numero=0, valor=9, tipo="yang", movil=True)
        else:
            # No debería pasar, pero fallback
            return LineaIChing(numero=0, valor=7, tipo="yang", movil=False)

    def generar_hexagrama(self, pregunta: str, semilla: Optional[int] = None) -> dict:
        """
        Genera un hexagrama completo lanzando 3 monedas × 6 líneas.
        Devuelve hexagrama primario y secundario (si hay líneas móviles).
        """
        if semilla:
            random.seed(semilla)

        # Generar 6 líneas de abajo a arriba
        lineas = []
        for i in range(6):
            _, _, _, suma = self.lanzar_tres_monedas()
            linea = self.suma_a_linea(suma)
            linea.numero = i + 1  # Líneas 1-6
            lineas.append(linea)

        # Calcular número de hexagrama primario
        # Cada línea contribuye un bit: Yang=1, Yin=0
        # La línea 1 (inferior) es el bit menos significativo
        numero_primario = 0
        for i, linea in enumerate(lineas):
            bit = 1 if linea.tipo == "yang" else 0
            numero_primario += bit * (2 ** i)

        # Asegurar que esté en rango 1-64
        if numero_primario == 0:
            numero_primario = 2  # Todo Yin = Hexagrama 2
        elif numero_primario > 64:
            numero_primario = numero_primario % 64 or 1

        # Buscar datos del hexagrama primario
        datos_primario = HEXAGRAMAS.get(numero_primario, {
            "nombre": f"Hexagrama {numero_primario}",
            "dictamen": "Consulta el texto clásico para este hexagrama.",
            "imagen": "La imagen del momento se revela en la contemplación.",
        })

        hexagrama_primario = HexagramaIChing(
            numero=numero_primario,
            nombre=datos_primario["nombre"],
            dictamen=datos_primario["dictamen"],
            imagen=datos_primario["imagen"],
            lineas=lineas,
        )

        # Detectar líneas móviles
        lineas_moviles = [l for l in lineas if l.movil]

        # Generar hexagrama secundario (si hay líneas móviles)
        hexagrama_secundario = None
        if lineas_moviles:
            lineas_secundarias = []
            for linea in lineas:
                if linea.movil:
                    # Invertir: Yin→Yang, Yang→Yin
                    nuevo_tipo = "yang" if linea.tipo == "yin" else "yin"
                    lineas_secundarias.append(LineaIChing(
                        numero=linea.numero,
                        valor=7 if nuevo_tipo == "yang" else 8,
                        tipo=nuevo_tipo,
                        movil=False,
                    ))
                else:
                    lineas_secundarias.append(LineaIChing(
                        numero=linea.numero,
                        valor=linea.valor,
                        tipo=linea.tipo,
                        movil=False,
                    ))

            # Calcular número secundario
            numero_secundario = 0
            for i, linea in enumerate(lineas_secundarias):
                bit = 1 if linea.tipo == "yang" else 0
                numero_secundario += bit * (2 ** i)

            if numero_secundario == 0:
                numero_secundario = 2
            elif numero_secundario > 64:
                numero_secundario = numero_secundario % 64 or 1

            datos_secundario = HEXAGRAMAS.get(numero_secundario, {
                "nombre": f"Hexagrama {numero_secundario}",
                "dictamen": "Consulta el texto clásico para este hexagrama.",
                "imagen": "La transformación revela el camino.",
            })

            hexagrama_secundario = HexagramaIChing(
                numero=numero_secundario,
                nombre=datos_secundario["nombre"],
                dictamen=datos_secundario["dictamen"],
                imagen=datos_secundario["imagen"],
                lineas=lineas_secundarias,
                es_secundario=True,
            )

        # Textos de líneas móviles
        textos_lineas_moviles = {}
        for lm in lineas_moviles:
            textos = TEXTOS_LINEAS_MOVILES.get(numero_primario, {})
            texto = textos.get(lm.numero, FALLBACK_LINEA.get(lm.numero, "Transformación en este punto."))
            textos_lineas_moviles[lm.numero] = texto

        return {
            "pregunta": pregunta,
            "hexagrama_primario": hexagrama_primario.to_dict(),
            "hexagrama_secundario": hexagrama_secundario.to_dict() if hexagrama_secundario else None,
            "lineas_moviles": textos_lineas_moviles,
            "tiene_lineas_moviles": len(lineas_moviles) > 0,
            "num_lineas_moviles": len(lineas_moviles),
        }

    def obtener_datos_para_interpretacion(self, resultado: dict) -> dict:
        """Prepara datos estructurados para la interpretación IA."""
        hp = resultado["hexagrama_primario"]
        hs = resultado.get("hexagrama_secundario")

        return {
            "pregunta": resultado["pregunta"],
            "hexagrama_primario": {
                "numero": hp["numero"],
                "nombre": hp["nombre"],
                "dictamen": hp["dictamen"],
                "imagen": hp["imagen"],
            },
            "hexagrama_secundario": {
                "numero": hs["numero"],
                "nombre": hs["nombre"],
                "dictamen": hs["dictamen"],
            } if hs else None,
            "lineas_moviles": resultado.get("lineas_moviles", {}),
            "num_lineas_moviles": resultado.get("num_lineas_moviles", 0),
        }
