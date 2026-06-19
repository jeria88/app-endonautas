"""
visual_matrix.py — Matriz visual de las 78 cartas del Tarot de Marsella (Jodorowsky-Camoin).

Fuente principal: Alejandro Jodorowsky & Marianne Costa, "La Vía del Tarot".
Cotejado contra el libro el 2026-06-18. Correcciones aplicadas en esa fecha:
  RONDA 1 (primera sesión):
  — AM-00 El Loco: perro no muerde (apoya patas); palo del hatillo es azul cielo con remate en cuchara
  — AM-02 La Papisa: libro abierto (no cerrado); huevo blanco junto a ella; tres cruces en el pecho
  — AM-08 La Justicia: color violeta añadido; balanza asimétrica; nueve triángulos de armiño
  — AM-09 El Ermitaño: dos lunas naranja (nuca y manto); barba y cabello azules; guante azul; bastón rojo
  — AM-15 El Diablo: figura_mira corregida a "bizco"; diablillos (no pareja humana); cuerda naranja; múltiples caras
  — ME-BAS-12 Caballero de Bastos: caballo blanco (no azul)
  — ME-COP-12 Caballero de Copas: yegua azul; copa flotando sobre palma abierta
  — ME-ESP-12 Caballero de Espadas: semental azul; espada roja como lanza; aura amarilla en yelmo
  — ME-ORO-12 Caballero de Oros: yegua azul a paso medido; dos oros (en mano y en tierra)

  RONDA 3 (tercera sesión — segunda pasada completa cotejando cada capítulo con la matriz):
  — AM-00 El Loco: bastón rojo (tres puntos/triángulo) separado del palo azul del hatillo; zapatos rojos; gorro: luna amarilla/círculo naranja (cielo) + luna en bola roja (abajo); cascabel blanco dividido por tres líneas
  — AM-01 El Mago: varita azul en mano IZQUIERDA (no derecha); copa y cuchillo como objetos sobre la mesa
  — AM-07 El Carro: símbolo del oro alquímico en el pecho de los caballos
  — AM-10 La Rueda: manivela en el centro exacto; corona de cinco puntas en la esfinge azul
  — AM-11 La Fuerza: ocho puntos en el belfo del animal; celosía en el pecho (4 trazos materiales + 5 espirituales)
  — AM-13 Arcano XIII: letras YHVH discernibles en el cráneo/nuca; pierna y brazo bañados de azul cielo; dos plantas brotando del suelo negro (azul oscuro + amarilla)
  — AM-16 La Torre: forma fetal en la llamarada; luz amarilla interior visible por puerta entreabierta; colores completos de la entidad fulgurante
  — AM-17 La Estrella: un árbol de fronda naranja tiene frutos amarillos
  — AM-18 La Luna: cangrejo sostiene DOS bolas (no una); orejas con color complementario (yin-yang); blasón de tres bandas entre patas de los perros; gotas de colores que descienden de la luna

  RONDA 2 (segunda sesión — revisión completa de arcanos mayores y figuras de corte):
  — AM-01 El Mago: varita azul; mesa 3 patas color carne; dados; cola serpiente naranja; 8 círculos naranja en cabello; sexto dedo
  — AM-03 La Emperatriz: cetro en zona del sexo; pirámide con puerta; serpiente blanca; luna creciente en vestido; pila bautismal
  — AM-04 El Emperador: piernas cuadrado blanco; casco con compás; collar espigas; medallón cruz verde; águila hembra incubando
  — AM-05 El Papa: mano azul/guante sujeta báculo; mitra 4 niveles; cintas rojas; zona azul en barba; escala en trono
  — AM-06 El Enamorado (singular): 5 manos; brazo compartido; cofia violeta; sol blanco casi invisible; zapatos rojos central
  — AM-07 El Carro (CRÍTICO): "esfinges" → DOS CABALLOS AZUL CIELO; bola blanca en mano der.; cetro carne en mano izq.; 12 estrellas
  — AM-10 La Rueda de Fortuna (CRÍTICO): "Anubis+esfinge" → TRES ANIMALES (carne/amarillo/azul-esfinge); rueda doble roja+amarilla
  — AM-11 La Fuerza: sombrero alado (no de infinito); pie 6 dedos; uñas rojas; 6 dientes negros; suelo amarillo labrado
  — AM-12 El Colgado: dintel carne; cuerda doble; nudo con triángulo; bolsillos media luna; 10 botones; 12 ramas sangrientas
  — AM-13 El Arcano XIII: esqueleto COLOR CARNE (no negro); guadaña mango amarillo+hoja azul-rojo; flauta 7 agujeros; ouroboros en ojo
  — AM-14 Templanza: alas azul cielo; pupilas amarillas; flor 5 pétalos; 2 serpientes a pies; 4 triángulos pecho; zapato violeta
  — AM-16 La Torre: personajes BOCA ABAJO (como el Colgado, no cayendo); puerta verde con luna; ladrillos carne; 3 escalones
  — AM-17 La Estrella: 8 estrellas iguales; jarra soldada a pelvis; luna naranja en frente; pájaro negro en árbol naranja
  — AM-18 La Luna: luna creciente de PERFIL; perro azul claro (cola alta, lengua verde) vs. perro carne (cola baja, lengua roja)
  — AM-19 El Sol: 2 personajes adultos (no niños) con rabo/puntos; collares rojos (restos de El Diablo); muro; sol bizquea
  — AM-20 El Juicio: bandera cruz carne en naranja; ser central con disco azul (vacío mental); tonsura espiral; 22 escalones; huevo oro
  — AM-21 El Mundo: figura mira a la IZQUIERDA; frasco+vara (yin/yang); estola azul→roja; huevo bajo lazo amarillo; animal sin aureola
  — ME-BAS-11 Sota Bastos: basto rústico sin labrar; postura de duda
  — ME-BAS-13 Reina Bastos: basto tallado; dos manos sobre el vientre + tercera mano artificial
  — ME-COP-11 Sota Copas: vaso simple de color carne (no copa dorada)
  — ME-ESP-13 Reina Espadas: espada activa (roja); escudo sobre el vientre
  — ME-ORO-11 Sota Oros: oro pequeño en mano; otro oro enterrado en tierra
  — ME-ORO-14 Rey Oros: dos oros (uno en mano, otro flotando en el aire)

verificado=True → confirmado contra el mazo físico.
verificado=False → cotejado con el libro Jodorowsky; pendiente de verificación contra el mazo real.

Estructura de cada entrada:
    colores      lista ordenada por presencia dominante (el primero domina)
    figura_mira  dirección de la figura principal ("derecha", "izquierda", "frente",
                 "sin figura — naipe numeral", etc.)
    gesto        descripción literal de lo que se ve (sin interpretación)
    simbolos     lista de elementos iconográficos reconocibles
    verificado   bool — True si fue cotejado contra el mazo físico

Helpers:
    get_visual(card_id) → dict {colores, figura_mira, gesto, simbolos} sin "verificado"
    cards_pending_verification() → lista de IDs con verificado=False
"""

VISUAL_MATRIX: dict[str, dict] = {

    # ── ARCANOS MAYORES ──────────────────────────────────────────────────────

    "AM-00": {  # El Loco — cotejado con libro Jodorowsky cap. El Loco
        "colores":     ["rojo", "verde", "azul claro", "amarillo claro", "carne"],
        "figura_mira": "derecha",
        "gesto":       "camina con paso resuelto, calzado de rojo, hundiendo en el suelo un bastón rojo; el palo que lleva el hatillo es azul cielo con remate en cuchara (receptivo); una hojita verde oculta en la mano que lo sujeta; el animal (perro/perra) apoya sus patas en la base de su columna, representado en azul claro",
        "simbolos":    ["bastón rojo (para caminar) — tiene tres puntos formando un pequeño triángulo", "palo azul cielo con remate en cuchara (para el hatillo)", "hatillo color carne iluminado por luz amarilla", "cascabeles en el traje", "cascabel blanco dividido por tres líneas", "animal azul claro apoyando patas (no muerde)", "mangas azul cielo", "gorro amarillo con dos medias lunas: luna amarilla en círculo naranja (vuelta hacia el cielo) + luna en bola roja en la punta trasera (vuelta hacia abajo)", "hoja verde en la mano", "cinturón con cuatro cascabeles amarillos", "zapatos rojos"],
        "verificado":  False,
    },
    "AM-01": {  # El Mago — cotejado con libro Jodorowsky cap. El Mago
        "colores":     ["rojo", "amarillo claro", "naranja", "carne", "azul claro"],
        "figura_mira": "derecha",
        "gesto":       "de pie junto a mesa de color carne con 3 patas; varita azul en la mano IZQUIERDA (palo activo, apunta al cielo); moneda/oro en la mano derecha; sombrero en espiral; cola de serpiente naranja visible a la altura del sexo; zapatos amarillos; un arbolito amarillo entre los pies",
        "simbolos":    ["varita azul en la mano izquierda (palo activo — apunta al cielo)", "moneda/oro amarillo en la mano derecha", "mesa color carne de 3 patas (con copa, cuchillo y dados encima)", "copa sobre la mesa", "cuchillo/espada pequeño sobre la mesa", "tres dados (caras 1, 2, 4)", "sombrero en espiral", "ocho círculos naranja en el cabello amarillo", "cabello amarillo", "cinturón doble", "zapatos amarillos", "arbolito amarillo entre los pies", "cola de serpiente naranja a nivel del sexo", "sexto dedo de color carne"],
        "verificado":  False,
    },
    "AM-02": {  # La Papisa — cotejado con libro Jodorowsky
        "colores":     ["azul oscuro", "rojo", "amarillo claro", "blanco", "carne"],
        "figura_mira": "frente",
        "gesto":       "sentada junto a un huevo blanco; sostiene libro abierto de color carne sobre el regazo sin leerlo; boca sellada; tiara con punta naranja tocando el borde de la carta",
        "simbolos":    ["huevo blanco oval (gestación)", "libro abierto color carne con 17 líneas", "tiara cuádruple con punta naranja", "cortina que se enrolla hacia el interior", "tres cruces en el pecho", "velo blanco detrás"],
        "verificado":  False,
    },
    "AM-03": {  # La Emperatriz — cotejado con libro Jodorowsky cap. La Emperatriz
        "colores":     ["rojo", "azul claro", "amarillo claro", "verde", "blanco", "carne"],
        "figura_mira": "derecha",
        "gesto":       "sentada en trono con cetro apoyado en la zona del sexo (no en la mano); escudo con águila en formación (un ala incompleta) en la otra mano; luna creciente en el vestido rojo; serpiente blanca a los pies; pila bautismal junto a ella; suelo embaldosado de colores",
        "simbolos":    ["cetro apoyado en zona del sexo con hojita verde bajo la mano", "escudo con águila de ala incompleta (en formación)", "luna creciente en vestido rojo", "ojos verdes", "nuez viril en el cuello", "pirámide amarilla con puerta en el pecho", "serpiente blanca a los pies", "pila bautismal", "suelo embaldosado de colores", "corona real"],
        "verificado":  False,
    },
    "AM-04": {  # El Emperador — cotejado con libro Jodorowsky cap. El Emperador
        "colores":     ["rojo", "azul claro", "amarillo claro", "verde", "naranja", "carne"],
        "figura_mira": "derecha",
        "gesto":       "sentado de perfil; piernas forman un cuadrado blanco; sostiene bastón similar al de la Emperatriz; barba y cabello azul cielo; casco amarillo con compás naranja; collar amarillo con espigas; medallón con cruz verde en el pecho",
        "simbolos":    ["piernas formando cuadrado blanco", "bastón similar al de la Emperatriz", "barba y cabello azul cielo", "casco amarillo con compás naranja", "collar amarillo con espigas", "medallón con cruz verde", "escudo con águila hembra incubando huevo", "símbolo de oro alquímico en hombro izquierdo", "corona"],
        "verificado":  False,
    },
    "AM-05": {  # El Papa — cotejado con libro Jodorowsky cap. El Papa
        "colores":     ["rojo", "azul claro", "amarillo claro", "blanco", "verde", "naranja", "carne"],
        "figura_mira": "frente",
        "gesto":       "mano azul cielo (con guante) sujeta báculo de tres niveles; mano de color carne bendice levantando dedos; dos acólitos con tonsuras opuestas (una abierta, una cerrada) se inclinan ante él; cabello blanco con dos cintas rojas; barba con zona azul cielo alrededor de la boca",
        "simbolos":    ["báculo de tres niveles", "mano azul cielo con guante sujetando báculo", "mano de color carne bendiciendo", "mitra de cuatro niveles con círculo naranja tocando el borde superior", "cabello blanco con dos cintas rojas", "barba con zona azul cielo alrededor de la boca", "cierre verde bajo la barba", "respaldo del trono en forma de escala", "dos acólitos con tonsuras opuestas"],
        "verificado":  False,
    },
    "AM-06": {  # El Enamorado (singular) — cotejado con libro Jodorowsky cap. El Enamorado
        "colores":     ["rojo", "azul claro", "amarillo claro", "violeta", "carne", "verde"],
        "figura_mira": "frente",
        "gesto":       "joven central en encrucijada entre dos mujeres (una a cada lado); comparten un brazo (brazo compartido entre figuras); Cupido apunta su flecha desde nube en lo alto; tierra labrada bajo los pies; zapatos rojos del personaje central; sol blanco casi invisible en lo alto",
        "simbolos":    ["Cupido con flecha desde nube", "cinco manos en diversas posiciones", "brazo compartido entre figuras", "tierra labrada bajo los pies", "cofia de 4 flores de 5 pétalos con centro violeta (mujer derecha)", "corona de hojas verdes (mujer izquierda)", "zapatos rojos del personaje central", "manchas azul cielo y rojo entre piernas (unión)", "sol blanco casi invisible arriba"],
        "verificado":  False,
    },
    "AM-07": {  # El Carro — cotejado con libro Jodorowsky cap. El Carro
        "colores":     ["rojo", "azul claro", "amarillo claro", "naranja", "verde", "carne"],
        "figura_mira": "frente",
        "gesto":       "príncipe armado sobre vehículo cuadrado color carne sin ruedas (hundido en la tierra); dos caballos de pelaje azul cielo (NO esfinges); sin riendas; cetro color carne en mano izquierda; bola/huevo blanco en mano derecha; 12 estrellas sobre el dosel",
        "simbolos":    ["dos caballos de pelaje azul cielo (no esfinges)", "caballo derecho con largas pestañas y ojo cerrado (femenino)", "símbolo del oro alquímico en el pecho de los caballos", "vehículo cuadrado color carne sin ruedas", "dosel con 12 estrellas", "cetro color carne en mano izquierda", "bola/huevo blanco en mano derecha", "sin riendas", "gota verde en blasón amarillo y naranja", "plantas rojas al pie del carro", "hombreras con rostros", "yelmo coronado"],
        "verificado":  False,
    },
    "AM-08": {  # La Justicia — cotejado con libro Jodorowsky
        "colores":     ["rojo", "azul claro", "amarillo claro", "violeta", "carne"],
        "figura_mira": "frente",
        "gesto":       "sentada asimétricamente en trono; balanza en mano izquierda cuyos platillos no están al mismo nivel; espada en la derecha NO paralela al eje del trono; collar sube más por la derecha; mancha violeta bajo el codo derecho",
        "simbolos":    ["balanza asimétrica (platillos a distinto nivel)", "espada no paralela al trono", "nueve triángulos de armiño sobre fondo azul en el traje", "mancha violeta bajo codo derecho (la mayor del Tarot)", "collar que sube más por la derecha", "esfera anaranjada en pilar derecho", "corona con tercer ojo amarillo-rojo"],
        "verificado":  False,
    },
    "AM-09": {  # El Ermitaño — cotejado con libro Jodorowsky
        "colores":     ["azul oscuro", "rojo", "amarillo claro", "naranja", "carne"],
        "figura_mira": "izquierda abajo (mirada perdida en la lejanía)",
        "gesto":       "anciano encorvado camina de perfil con bastón rojo; sostiene linterna encendida hacia adelante con guante azul; espalda encorvada concentra toda la memoria de su pasado",
        "simbolos":    ["linterna encendida", "bastón rojo", "guante azul", "barba y cabello azules", "dos lunas naranja (una en la nuca, otra en el reverso del manto)", "capucha", "múltiples capas de ropa con rayas (experiencia acumulada)"],
        "verificado":  False,
    },
    "AM-10": {  # La Rueda de Fortuna — cotejado con libro Jodorowsky cap. La Rueda de Fortuna
        "colores":     ["rojo", "azul claro", "amarillo", "añil", "violeta", "carne", "negro"],
        "figura_mira": "ninguna figura central — tres animales en la rueda",
        "gesto":       "rueda doble (círculo rojo y amarillo) gira; tres animales la recorren; animal color carne desciende; animal amarillo asciende; animal azul-esfinge preside la cima; suelo azul claro ondulado (movedizo)",
        "simbolos":    ["rueda doble (círculo rojo y amarillo)", "manivela en el centro exacto de la rueda", "animal color carne descendiendo (parte inferior cubierta)", "animal amarillo ascendiendo (vestido de cintura para arriba, orejas tapadas)", "animal azul con aspecto de esfinge en la cima (capa roja en forma de corazón, sostiene espada, manchas moradas/violeta, óvalo añil en frente como tercer ojo, corona de cinco puntas)", "suelo azul claro ondulado (movedizo)"],
        "verificado":  False,
    },
    "AM-11": {  # La Fuerza — cotejado con libro Jodorowsky cap. La Fuerza
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne", "verde"],
        "figura_mira": "izquierda",
        "gesto":       "mujer con sombrero alado (6 puntas rojas, plumas de águila) abre/cierra suavemente las fauces del león con ambas manos; pie con seis dedos; cabeza de la bestia al nivel de la pelvis; suelo amarillo labrado sin paisaje",
        "simbolos":    ["sombrero alado con plumas de águila y 6 puntas rojas (corresponden a los 6 dientes del león)", "pie con seis dedos", "uñas rojas", "león con seis dientes negros", "ocho puntos en el belfo (hocico) del animal", "celosía en el pecho de la mujer (4 trazos materiales + 5 trazos espirituales)", "cabeza de la bestia al nivel de la pelvis de la mujer", "suelo amarillo labrado (sin fondo de paisaje)", "guirnalda de flores"],
        "verificado":  False,
    },
    "AM-12": {  # El Colgado — cotejado con libro Jodorowsky cap. El Colgado
        "colores":     ["rojo", "azul claro", "amarillo claro", "amarillo oscuro", "carne"],
        "figura_mira": "frente (boca abajo)",
        "gesto":       "joven cuelga boca abajo de un pie desde dintel color carne; piernas forman triángulo; brazos ocultos tras la espalda; bolsillos en forma de media luna; cuerda doble (un extremo fálico, otro femenino); cabello multicolor con símbolo solar",
        "simbolos":    ["dintel color carne", "pie atado con cuerda doble (extremo fálico + extremo femenino)", "triángulo inscrito en círculo en el nudo del talón", "triángulo de piernas", "bolsillos en forma de media luna (uno receptivo, uno activo)", "cabello con mechas amarillo oscuro + símbolo solar redondo + luna en amarillo claro", "diez botones con significados cabalísticos", "doce ramas cortadas con doce heridas sangrientas"],
        "verificado":  False,
    },
    "AM-13": {  # El Arcano XIII — cotejado con libro Jodorowsky cap. XIII
        "colores":     ["carne", "negro", "rojo", "amarillo claro", "azul claro", "blanco"],
        "figura_mira": "derecha",
        "gesto":       "esqueleto de color CARNE siega horizontalmente con guadaña (mango amarillo, hoja azul claro y rojo); suelo negro; de la tierra brotan dos cabezas, manos y pies; rostro = sombra de perfil; sin nombre escrito",
        "simbolos":    ["esqueleto de color carne (énfasis: no negro)", "guadaña con mango amarillo y hoja azul claro y rojo", "suelo negro", "dos cabezas en el suelo", "manos y pies cortados en el suelo", "hueso blanco con 7 agujeros (flauta)", "rostro como sombra de perfil", "ojo como dragón mordiéndose la cola (ouroboros)", "cabeza con forma lunar", "letras YHVH (Yod He Vav He) discernibles entre las rayas del cráneo/nuca", "pierna y brazo del esqueleto bañados de azul cielo", "pelvis y columna azul cielo y rojo", "espiga de trigo hasta flor roja de 4 pétalos", "dos plantas/hierbas brotando del suelo negro: una azul oscuro (espiritualidad intuitiva) y una amarilla (inteligencia solar)", "trébol rojo en rodilla y codo"],
        "verificado":  False,
    },
    "AM-14": {  # La Templanza — cotejado con libro Jodorowsky cap. Templanza
        "colores":     ["rojo", "azul claro", "amarillo claro", "violeta", "carne", "verde"],
        "figura_mira": "ligeramente derecha",
        "gesto":       "ángel andrógino de alas azul cielo vierte líquido entre dos copas sin derramar; pupilas amarillas; flor roja de 5 pétalos en la cabeza; cabello amarillo; punta de zapato violeta; dos serpientes entrelazadas a los pies; mano sobre el pecho",
        "simbolos":    ["alas azul cielo", "pupilas amarillas", "flor roja de 5 pétalos en la cabeza", "cabello amarillo", "dos copas (vierte sin derramar)", "4 triángulos amarillos en el pecho", "círculo amarillo con triángulo inscrito encima del pecho", "mano en el pecho", "punta de zapato violeta", "dos serpientes entrelazadas a los pies"],
        "verificado":  False,
    },
    "AM-15": {  # El Diablo — cotejado con libro Jodorowsky (cuerpo azul cielo confirmado)
        "colores":     ["azul claro", "negro", "rojo", "naranja", "amarillo claro", "carne"],
        "figura_mira": "frente (bizco — mira fijamente su propia nariz)",
        "gesto":       "demonio de cuerpo azul cielo sobre pedestal; bizquea mirando su nariz; yergue antorcha con mango verde; dos diablillos (uno femenino izq., uno masculino der.) atados con cuerda naranja que pasa por anillo central azul cielo; sus pies se enraízan en el suelo negro",
        "simbolos":    ["cuerpo azul cielo del demonio", "antorcha con mango verde y llama roja", "cuerda naranja atando a dos diablillos", "anillo central azul cielo", "dos pechos con ojos (carácter emocional)", "cara con lengua en el vientre (deseo sexual)", "ojos en las rodillas (vida material)", "sexo como tercera lengua", "alas de murciélago", "cuernos", "pezuñas", "pies enraizados en negro"],
        "verificado":  True,
    },
    "AM-16": {  # La Torre — cotejado con libro Jodorowsky cap. La Torre
        "colores":     ["rojo", "azul claro", "amarillo claro", "naranja", "negro", "verde", "carne"],
        "figura_mira": "figuras cabeza abajo (como el Colgado)",
        "gesto":       "rayo/entidad fulgurante golpea la corona de la torre haciéndola volar; dos figuras NO caen sino están boca abajo (como el Colgado) con cabello amarillo, tocando plantas verdes; ladrillos color carne; tres escalones; puerta verde con media luna en la base",
        "simbolos":    ["entidad fulgurante multicolor (llamarada/pájaro de fuego — lleva todos los colores: amarillo, rojo, verde, carne, azul)", "forma fetal discernible en la llamarada (germen de nueva consciencia)", "corona volando", "dos figuras boca abajo con cabello amarillo (tocando plantas verdes)", "un personaje con pies hacia el cielo", "ladrillos color carne", "tres escalones", "puerta verde con media luna (receptividad) — entreabierta deja ver luz amarilla interior", "gotas de colores en el aire (amarillas, rojas, azules, verdes)", "manchas amarillas en el suelo"],
        "verificado":  False,
    },
    "AM-17": {  # La Estrella — cotejado con libro Jodorowsky cap. La Estrella
        "colores":     ["azul claro", "naranja", "rojo", "amarillo claro", "verde", "negro", "carne"],
        "figura_mira": "abajo",
        "gesto":       "mujer desnuda arrodillada con luna naranja en la frente; una jarra soldada a la pelvis vierte al estanque; otra jarra en el paisaje; rodilla ligeramente deforme; ocho estrellas arriba; pájaro negro en cima de árbol de fronda naranja",
        "simbolos":    ["ocho estrellas iguales (sin distinción de tamaño)", "jarra soldada a la pelvis (vierte al estanque)", "jarra en el paisaje", "luna naranja en la frente", "símbolo en el ombligo (germen de vida)", "rodilla ligeramente deforme (semeja nalgas de bebé)", "árboles de fronda naranja — uno tiene frutos amarillos", "pájaro negro en cima del árbol naranja", "pechos desnudos", "estanque"],
        "verificado":  False,
    },
    "AM-18": {  # La Luna — cotejado con libro Jodorowsky cap. La Luna
        "colores":     ["azul claro", "naranja", "rojo", "amarillo claro", "verde", "carne"],
        "figura_mira": "luna creciente de perfil (no frontal); cangrejo mira arriba",
        "gesto":       "luna creciente de perfil derrama rayos naranja (primero plano) y rayos rojos (segundo plano); cangrejo sostiene bola azul en pinzas; perro azul claro (lengua verde, cola levantada) frente a torre abierta; perro color carne (cola baja, lengua roja) frente a torre cerrada; tres escalones blancos; dos orillas distintas del estanque",
        "simbolos":    ["luna creciente de perfil (no frontal)", "rayos naranja en primer plano", "rayos rojos en segundo plano", "gotas de colores que descienden de la luna hacia los animales", "fondo azul cielo", "perro azul claro (lengua verde, cola levantada, torre abierta detrás) — oreja de color complementario (carne)", "perro color carne (cola baja, lengua roja, torre cerrada detrás) — oreja de color complementario (azul)", "cangrejo con DOS pequeñas bolas en las pinzas (ofrendas)", "blasón de tres bandas entre patas de los perros: superior verde oscuro / medio dos plantas / inferior tres gotas rojas", "dos torres distintas (una abierta con almenas receptivas, una cerrada)", "tres escalones blancos al pie de la torre cerrada", "dos orillas distintas del estanque (salvaje vs. bordeada de líneas negras/azules)"],
        "verificado":  False,
    },
    "AM-19": {  # El Sol — cotejado con libro Jodorowsky cap. El Sol
        "colores":     ["amarillo claro", "rojo", "azul claro", "naranja", "blanco", "carne"],
        "figura_mira": "sol mira de frente (bizquea ligeramente); personajes de frente",
        "gesto":       "dos personajes en un río azul claro bajo el sol; el de la izquierda tiene un rabo (vestigio animal); el de la derecha lleva tres puntos en el costado; collares rojos en ambos cuellos (restos de la cuerda de El Diablo); muro amarillo y rojo en segundo plano (nueva construcción); tierra blanca a la derecha (purificada)",
        "simbolos":    ["sol que nos mira de frente (bizquea ligeramente como El Diablo)", "rayos retorcidos amarillos y rayos rectos rojos", "ojos blancos con pupilas negras en el sol", "río azul claro", "dos personajes (no niños): el izq. con rabo; el der. con tres puntos en el costado", "collares rojos en ambos cuellos (restos de los lazos de El Diablo)", "taparrabos color azul", "muro amarillo y rojo en segundo plano", "tierra blanca a la derecha", "cinco gotas azul claro ascendiendo hacia el sol", "banda verde de fertilidad"],
        "verificado":  False,
    },
    "AM-20": {  # El Juicio — cotejado con libro Jodorowsky cap. El Juicio
        "colores":     ["rojo", "azul claro", "naranja", "amarillo claro", "carne"],
        "figura_mira": "ángel mira de frente; mujer mira al hombre/hijo; hombre mira al ángel",
        "gesto":       "ángel toca trompeta desde nube circular azul cielo; bandera con cruz de color carne sobre fondo naranja dividido en cuatro cuadrados; ser central emerge de la tierra con disco azul central (vacío mental); la mujer (izquierda) toca con el codo al ser central; el hombre (derecha) mira al ángel; tonsura del ser azul en espiral; veintidós escalones en la trompeta; huevo de oro en el pabellón de la trompeta",
        "simbolos":    ["ángel con trompeta (nos mira de frente)", "nube circular azul cielo rodeando al ángel", "bandera con cruz de color carne sobre fondo naranja en cuatro cuadrados", "ser central emergiendo de la tierra con disco azul giratorio en la cabeza (vacío mental)", "tonsura en espiral del ser central", "veintidós escalones en la trompeta", "huevo de oro en el pabellón de la trompeta", "mujer (izquierda) que toca con el codo al ser central", "hombre (derecha) mirando al ángel"],
        "verificado":  False,
    },
    "AM-21": {  # El Mundo — cotejado con libro Jodorowsky cap. El Mundo
        "colores":     ["rojo", "azul claro", "amarillo claro", "verde", "blanco", "carne"],
        "figura_mira": "izquierda (receptividad)",
        "gesto":       "figura femenina danza mirando hacia la IZQUIERDA dentro de mandorla oval de hojas azul claro; mano derecha sostiene frasco (receptivo); mano izquierda sostiene vara (activo); estola azul (atrás) pasa por delante volviéndose roja; pie apoyado en suelo rojo labrado con seis surcos; huevo blanco disimulado por lazo amarillo en la parte baja de la mandorla",
        "simbolos":    ["mandorla oval de hojas azul claro", "figura danzante mirando a la izquierda", "frasco en mano derecha (principio receptivo)", "vara en mano izquierda (principio activo)", "estola azul detrás que se vuelve roja al pasar por delante", "pie en suelo rojo labrado con 6 surcos", "huevo blanco disimulado por lazo amarillo (parte baja de la mandorla)", "ángel (arriba izquierda, con aureola)", "águila (arriba derecha, con aureola)", "león (abajo derecha, con aureola)", "animal color carne (abajo izquierda, SIN aureola — caballo/buey/unicornio, posible cuerno sobre el ojo)"],
        "verificado":  False,
    },

    # ── ARCANOS MENORES — BASTOS ─────────────────────────────────────────────
    # Colores: rojo (bastos), negro (extremos), azul claro (ornamentos)
    # Sin figuras en numerales 1-10; con personaje en 11-14.

    "ME-BAS-01": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Un bastón único vertical en posición central — todo el espacio lo sostiene",
        "simbolos":    ["bastón rojo con extremos negros", "ornamentos vegetales azules"],
        "verificado":  False,
    },
    "ME-BAS-02": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Dos bastos verticales paralelos, uno a cada lado, sin cruzarse",
        "simbolos":    ["dos bastos paralelos", "ornamentos azules entre ellos"],
        "verificado":  False,
    },
    "ME-BAS-03": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Tres bastos: dos verticales con uno diagonal cruzándolos al centro",
        "simbolos":    ["dos bastos verticales", "bastón diagonal central", "primer cruzamiento"],
        "verificado":  False,
    },
    "ME-BAS-04": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Cuatro bastos: dos pares cruzados formando una X doble",
        "simbolos":    ["dos pares cruzados en X", "ornamentos en los cuatro cuadrantes"],
        "verificado":  False,
    },
    "ME-BAS-05": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Cinco bastos en cruzamiento complejo — el quinto atraviesa el centro",
        "simbolos":    ["cuatro bastos cruzados", "bastón central atravesando el nudo"],
        "verificado":  False,
    },
    "ME-BAS-06": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Seis bastos en tres pares cruzados, patrón simétrico de dos filas",
        "simbolos":    ["tres pares cruzados", "simetría en dos filas", "ornamentos azules"],
        "verificado":  False,
    },
    "ME-BAS-07": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Siete bastos en patrón denso: tres pares más un bastón diagonal central",
        "simbolos":    ["tres pares cruzados", "bastón diagonal extra", "densidad creciente"],
        "verificado":  False,
    },
    "ME-BAS-08": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Ocho bastos en cruzamiento muy denso — cuatro pares entrelazados",
        "simbolos":    ["cuatro pares entrelazados", "máxima complejidad del octavo"],
        "verificado":  False,
    },
    "ME-BAS-09": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Nueve bastos: máxima complejidad antes del cierre — cruzamientos en cuadrícula",
        "simbolos":    ["cuadrícula de cruzamientos", "patrón casi saturado"],
        "verificado":  False,
    },
    "ME-BAS-10": {
        "colores":     ["rojo", "negro", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Diez bastos entrelazados en patrón saturado — el palo carga todo su peso",
        "simbolos":    ["entrelazado saturado", "sin espacio libre entre los bastos"],
        "verificado":  False,
    },
    "ME-BAS-11": {  # Sota de Bastos — Jodorowsky: basto rústico sin labrar
        "colores":     ["rojo", "azul claro", "carne"],
        "figura_mira": "derecha",
        "gesto":       "joven de pie duda si alzar o no el bastón; postura entre la acción y la inacción; basto rústico y natural (sin tallar)",
        "simbolos":    ["bastón rústico sin labrar (orgánico, natural)", "postura de duda activa", "sombrero con pluma", "botas"],
        "verificado":  False,
    },
    "ME-BAS-12": {  # Caballero de Bastos — caballo blanco (confirmado Jodorowsky)
        "colores":     ["blanco", "rojo", "azul claro", "amarillo claro", "carne"],
        "figura_mira": "derecha (galope)",
        "gesto":       "jinete sobre caballo blanco (sublimación del deseo) al galope con bastón en alto; el basto atraviesa su mano indicando unidad total con su energía",
        "simbolos":    ["caballo blanco (semejante a un semental)", "bastón natural atravesando la mano", "yelmo con pluma", "armadura parcial"],
        "verificado":  False,
    },
    "ME-BAS-13": {  # Reina de Bastos — Jodorowsky: basto tallado; tercera mano artificial
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne"],
        "figura_mira": "derecha",
        "gesto":       "sentada con las dos manos sobre el vientre (centro sexual y creativo) y una tercera mano artificial; bastón tallado (trabajado, no rústico); totalmente inmersa en su palo",
        "simbolos":    ["bastón tallado (no rústico)", "dos manos sobre el vientre (centro sexual-creativo)", "tercera mano artificial", "trono ornamentado", "corona floral"],
        "verificado":  False,
    },
    "ME-BAS-14": {  # Rey de Bastos
        "colores":     ["rojo", "azul claro", "amarillo claro"],
        "figura_mira": "derecha",
        "gesto":       "entronado sostiene bastón largo y cetro; expresión de autoridad plena",
        "simbolos":    ["bastón largo", "cetro", "trono", "corona real", "manto"],
        "verificado":  False,
    },

    # ── ARCANOS MENORES — COPAS ──────────────────────────────────────────────
    # Copas doradas (amarillo claro) con interior rojo. Fondo crema.
    # Verificados: ME-COP-01 a ME-COP-10 (numerales).

    "ME-COP-01": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Una copa monumental al centro — el As tiene forma de catedral gótica con arco",
        "simbolos":    ["copa dorada forma catedral gótica", "arco ornamentado", "interior rojo"],
        "verificado":  True,
    },
    "ME-COP-02": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Dos copas simétricas: una arriba, una abajo, enfrentadas en eje vertical",
        "simbolos":    ["dos copas doradas enfrentadas", "interior rojo", "ornamentos florales"],
        "verificado":  True,
    },
    "ME-COP-03": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Tres copas: una arriba, dos abajo, formando triángulo",
        "simbolos":    ["triángulo de copas doradas", "interior rojo en cada copa"],
        "verificado":  True,
    },
    "ME-COP-04": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Cuatro copas: dos arriba, dos abajo, en cuadrado simétrico",
        "simbolos":    ["cuatro copas en cuadrado", "interior rojo", "ornamentos entre ellas"],
        "verificado":  True,
    },
    "ME-COP-05": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Cinco copas: una al centro, cuatro en las esquinas formando cruz",
        "simbolos":    ["copa central", "cuatro copas en esquinas", "patrón de cruz"],
        "verificado":  True,
    },
    "ME-COP-06": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Seis copas: dos columnas de tres, simétricas",
        "simbolos":    ["dos columnas de tres copas doradas", "interior rojo", "simetría perfecta"],
        "verificado":  True,
    },
    "ME-COP-07": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Siete copas: tres arriba, una al centro, tres abajo — patrón 3-1-3",
        "simbolos":    ["patrón 3-1-3", "copa central destacada", "seis copas en dos filas"],
        "verificado":  True,
    },
    "ME-COP-08": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Ocho copas: dos columnas de cuatro, una a cada lado",
        "simbolos":    ["dos columnas de cuatro copas", "interior rojo", "fondo crema"],
        "verificado":  True,
    },
    "ME-COP-09": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Nueve copas: tres filas de tres, cuadrado perfecto",
        "simbolos":    ["cuadrado 3×3 de copas doradas", "interior rojo uniforme"],
        "verificado":  True,
    },
    "ME-COP-10": {
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Diez copas: dos filas de cinco — el ciclo del agua completo",
        "simbolos":    ["dos filas de cinco copas doradas", "interior rojo", "composición plena"],
        "verificado":  True,
    },
    "ME-COP-11": {  # Sota de Copas — Jodorowsky: vaso de color carne (simple, no dorado)
        "colores":     ["amarillo claro", "rojo", "azul claro", "carne"],
        "figura_mira": "izquierda",
        "gesto":       "joven mira hacia la izquierda dudando si abrir o cerrar su copa; sostiene un simple vaso de color carne (no cáliz dorado); postura entre el amor y el no-amor",
        "simbolos":    ["vaso simple de color carne (no copa dorada)", "postura de duda contemplativa (¿amar o no amar?)", "sombrero de perfil", "capa decorada"],
        "verificado":  False,
    },
    "ME-COP-12": {  # Caballero de Copas — yegua azul (confirmado Jodorowsky)
        "colores":     ["amarillo claro", "azul claro", "rojo", "carne"],
        "figura_mira": "derecha",
        "gesto":       "jinete sobre delicada yegua azul; lleva copa dorada flotando sobre la palma abierta (no la sujeta con los dedos); la copa guía al caballo y al jinete",
        "simbolos":    ["yegua azul delicada", "copa dorada flotando sobre palma abierta", "mano abierta (sin aferrar)", "yelmo emplumado", "armadura"],
        "verificado":  False,
    },
    "ME-COP-13": {  # Reina de Copas
        "colores":     ["amarillo claro", "azul claro", "rojo"],
        "figura_mira": "izquierda",
        "gesto":       "sentada sostiene copa dorada con tapa; mirada interior hacia la izquierda",
        "simbolos":    ["copa dorada con tapa", "trono ornamentado", "corona", "manto azul"],
        "verificado":  False,
    },
    "ME-COP-14": {  # Rey de Copas
        "colores":     ["amarillo claro", "azul claro", "rojo"],
        "figura_mira": "derecha",
        "gesto":       "entronado sostiene copa dorada y cetro; expresión serena y contenida",
        "simbolos":    ["copa dorada", "cetro", "trono", "corona real", "manto"],
        "verificado":  False,
    },

    # ── ARCANOS MENORES — ESPADAS ────────────────────────────────────────────
    # Espadas negras con guarda roja y azul. Se entrecruzan en disposición oval.

    "ME-ESP-01": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Una espada única vertical — hoja negra con guarda roja y azul al centro",
        "simbolos":    ["espada vertical única", "guarda roja y azul", "hoja negra"],
        "verificado":  False,
    },
    "ME-ESP-02": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Dos espadas cruzadas en X — guardas visibles en el punto de cruce",
        "simbolos":    ["dos espadas en X", "guardas rojas y azules en el cruce"],
        "verificado":  False,
    },
    "ME-ESP-03": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Tres espadas en disposición oval — una central rodeada de dos laterales",
        "simbolos":    ["espada central", "dos espadas laterales", "primer diseño oval"],
        "verificado":  False,
    },
    "ME-ESP-04": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Cuatro espadas: patrón oval simétrico, dos pares opuestos",
        "simbolos":    ["dos pares opuestos en oval", "guardas distribuidas"],
        "verificado":  False,
    },
    "ME-ESP-05": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Cinco espadas: entrelazado complejo, el quinto atraviesa el nudo central",
        "simbolos":    ["cuatro espadas en oval", "quinta espada atravesando el nudo", "tensión visual"],
        "verificado":  False,
    },
    "ME-ESP-06": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Seis espadas en oval denso — guardas rojas y azules distribuidas",
        "simbolos":    ["oval de seis espadas", "guardas rojas y azules visibles"],
        "verificado":  False,
    },
    "ME-ESP-07": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Siete espadas: el entrelazado se vuelve intrincado, casi laberíntico",
        "simbolos":    ["entrelazado laberíntico", "guardas apenas visibles entre las hojas"],
        "verificado":  False,
    },
    "ME-ESP-08": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Ocho espadas: patrón oval muy apretado — las guardas apenas se ven",
        "simbolos":    ["oval muy apretado", "hojas negras dominantes", "guardas apenas visibles"],
        "verificado":  False,
    },
    "ME-ESP-09": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Nueve espadas: máxima densidad del entrelazado, casi abstracto",
        "simbolos":    ["entrelazado casi abstracto", "negro dominante", "mínimo espacio libre"],
        "verificado":  False,
    },
    "ME-ESP-10": {
        "colores":     ["negro", "rojo", "azul claro"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Diez espadas: el palo en saturación — hojas negras dominan todo el espacio",
        "simbolos":    ["saturación de hojas negras", "palo en su máxima carga"],
        "verificado":  False,
    },
    "ME-ESP-11": {  # Sota de Espadas — verificado: mira hacia la izquierda
        "colores":     ["negro", "rojo", "azul claro", "carne"],
        "figura_mira": "izquierda",
        "gesto":       "joven mira hacia la izquierda mientras sostiene espada erguida con ambas manos",
        "simbolos":    ["espada erguida", "sombrero de perfil", "botas altas", "postura de guardia"],
        "verificado":  True,
    },
    "ME-ESP-12": {  # Caballero de Espadas — caballo azul (confirmado Jodorowsky)
        "colores":     ["rojo", "azul claro", "negro", "amarillo claro", "carne"],
        "figura_mira": "derecha (galope)",
        "gesto":       "jinete sobre semental azul al galope con espada roja (semejante a lanza) en alto en acción de corte; yelmo con aura amarilla símbolo de santidad",
        "simbolos":    ["semental azul", "espada roja que semeja lanza", "yelmo con aura amarilla", "armadura completa"],
        "verificado":  False,
    },
    "ME-ESP-13": {  # Reina de Espadas — Jodorowsky: escudo sobre el vientre; espada activa (roja)
        "colores":     ["rojo", "azul claro", "negro", "carne"],
        "figura_mira": "derecha",
        "gesto":       "sentada sostiene espada activa (roja) apuntando al cielo; lleva escudo sobre el vientre; mirada fría y directa; totalmente inmersa en lo intelectual",
        "simbolos":    ["espada activa (roja)", "escudo sobre el vientre", "trono", "corona", "manto"],
        "verificado":  False,
    },
    "ME-ESP-14": {  # Rey de Espadas
        "colores":     ["rojo", "azul claro", "negro"],
        "figura_mira": "derecha",
        "gesto":       "entronado con espada larga; mirada penetrante; figura de autoridad intelectual",
        "simbolos":    ["espada larga", "trono", "corona real", "manto"],
        "verificado":  False,
    },

    # ── ARCANOS MENORES — OROS ───────────────────────────────────────────────
    # Círculos dorados vacíos (sin número impreso). Fondo neutro.
    # Los Oros son el único palo sin numeración visible en los naipes.

    "ME-ORO-01": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Un oro grande único al centro — el círculo dorado más puro y solitario",
        "simbolos":    ["círculo dorado único", "ornamentos rojos y verdes alrededor"],
        "verificado":  False,
    },
    "ME-ORO-02": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Dos oros: uno arriba, uno abajo, en eje vertical simétrico",
        "simbolos":    ["dos círculos dorados en eje vertical", "ornamentos entre ellos"],
        "verificado":  False,
    },
    "ME-ORO-03": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Tres oros: triángulo — uno arriba, dos abajo",
        "simbolos":    ["triángulo de círculos dorados", "simetría triangular"],
        "verificado":  False,
    },
    "ME-ORO-04": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Cuatro oros: cuadrado — dos arriba, dos abajo",
        "simbolos":    ["cuadrado de cuatro círculos dorados", "composición estable"],
        "verificado":  False,
    },
    "ME-ORO-05": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Cinco oros: uno al centro, cuatro en las esquinas formando cruz",
        "simbolos":    ["oro central", "cuatro oros en esquinas", "patrón de cruz"],
        "verificado":  False,
    },
    "ME-ORO-06": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Seis oros: dos columnas de tres",
        "simbolos":    ["dos columnas de tres círculos dorados", "simetría perfecta"],
        "verificado":  False,
    },
    "ME-ORO-07": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Siete oros: tres arriba, uno al centro, tres abajo — patrón 3-1-3",
        "simbolos":    ["patrón 3-1-3", "oro central destacado", "seis oros en dos filas"],
        "verificado":  False,
    },
    "ME-ORO-08": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Ocho oros: dos columnas de cuatro",
        "simbolos":    ["dos columnas de cuatro círculos dorados", "equilibrio visual"],
        "verificado":  False,
    },
    "ME-ORO-09": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Nueve oros: tres filas de tres — cuadrado completo",
        "simbolos":    ["cuadrado 3×3 de círculos dorados", "plenitud material"],
        "verificado":  False,
    },
    "ME-ORO-10": {
        "colores":     ["amarillo claro", "rojo", "verde"],
        "figura_mira": "sin figura — naipe numeral",
        "gesto":       "Diez oros: dos filas de cinco — el ciclo de la tierra cumplido",
        "simbolos":    ["dos filas de cinco círculos dorados", "saturación armónica"],
        "verificado":  False,
    },
    "ME-ORO-11": {  # Sota de Oros — Jodorowsky: oro pequeño en mano; otro enterrado bajo tierra
        "colores":     ["amarillo claro", "azul claro", "rojo", "carne"],
        "figura_mira": "frente abajo",
        "gesto":       "joven contempla un pequeño oro que sostiene en la mano; otro oro aún enterrado bajo tierra como tesoro; duda entre guardar o gastar, ahorrar o invertir",
        "simbolos":    ["oro pequeño en la mano (visible)", "otro oro enterrado bajo tierra (tesoro oculto)", "postura de duda (¿guardar o gastar?)", "dos pies en tierra", "sombrero"],
        "verificado":  False,
    },
    "ME-ORO-12": {  # Caballero de Oros — yegua azul a paso medido (confirmado Jodorowsky)
        "colores":     ["amarillo claro", "azul claro", "rojo", "verde"],
        "figura_mira": "derecha (paso)",
        "gesto":       "jinete sobre yegua azul a pasos medidos y seguros; sostiene moneda de oro espiritualizada que flota en el aire; aspecto andrógino o hermafrodita",
        "simbolos":    ["yegua azul a pasos medidos (ni despacio ni deprisa)", "moneda dorada flotando en el aire", "segundo oro enterrado en la tierra", "aspecto andrógino", "yelmo"],
        "verificado":  False,
    },
    "ME-ORO-13": {  # Reina de Oros
        "colores":     ["rojo", "azul claro", "amarillo claro"],
        "figura_mira": "derecha",
        "gesto":       "sentada sostiene moneda con gesto de quien conoce su valor real",
        "simbolos":    ["moneda dorada", "trono ornamentado", "corona", "manto rojo"],
        "verificado":  False,
    },
    "ME-ORO-14": {  # Rey de Oros — Jodorowsky: dos oros (uno en mano, otro flotando)
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "derecha",
        "gesto":       "entronado domina dos oros: uno en la mano y otro que flota en el aire (oro espiritual); mirada hacia un más allá; conoce su reino pero contempla el exterior",
        "simbolos":    ["oro en la mano", "segundo oro flotando en el aire (espiritual)", "cetro", "trono", "corona imperial", "manto", "mirada hacia el exterior (conoce su reino pero busca el más allá)"],
        "verificado":  False,
    },
}


def get_visual(card_id: str) -> dict:
    """Retorna el visual dict (sin el campo verificado) para la carta dada."""
    entry = VISUAL_MATRIX.get(card_id)
    if not entry:
        return {}
    return {k: v for k, v in entry.items() if k != "verificado"}


def cards_pending_verification() -> list[str]:
    """Lista de IDs cuyo visual no ha sido cotejado contra el mazo físico."""
    return [cid for cid, v in VISUAL_MATRIX.items() if not v.get("verificado", False)]


def verification_summary() -> dict:
    """Resumen del estado de verificación."""
    total = len(VISUAL_MATRIX)
    verified = sum(1 for v in VISUAL_MATRIX.values() if v.get("verificado", False))
    return {
        "total": total,
        "verificadas": verified,
        "pendientes": total - verified,
        "porcentaje": round(verified / total * 100, 1),
    }
