"""
visual_matrix.py — Matriz visual de las 78 cartas del Tarot de Marsella (Jodorowsky-Camoin).

verificado=True → confirmado contra el mazo físico.
verificado=False → datos heredados; pendiente de auditoría contra el mazo real.

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

    "AM-00": {  # El Loco
        "colores":     ["rojo", "verde", "carne", "azul claro", "amarillo claro"],
        "figura_mira": "derecha",
        "gesto":       "camina alegremente con bastón y bolsa al hombro sin ver el abismo; un perro le muerde la ropa",
        "simbolos":    ["bastón con bolsa", "perro mordiéndo la ropa", "precipicio al borde", "flores en el bastón"],
        "verificado":  False,
    },
    "AM-01": {  # El Mago
        "colores":     ["rojo", "amarillo claro", "carne", "azul claro"],
        "figura_mira": "derecha",
        "gesto":       "señala al cielo con varita mientras la otra mano toca objetos sobre la mesa",
        "simbolos":    ["mesa con objetos", "varita", "copa", "cuchillo", "moneda", "dado", "sombrero de borde infinito"],
        "verificado":  False,
    },
    "AM-02": {  # La Papisa
        "colores":     ["azul oscuro", "rojo", "amarillo claro", "blanco"],
        "figura_mira": "frente",
        "gesto":       "sostiene libro cerrado sobre el regazo; velo blanco cae detrás; boca sellada",
        "simbolos":    ["libro cerrado", "tiara triple", "velo blanco", "columnas", "manto azul"],
        "verificado":  False,
    },
    "AM-03": {  # La Emperatriz
        "colores":     ["rojo", "azul claro", "amarillo claro", "verde", "carne"],
        "figura_mira": "derecha",
        "gesto":       "sentada en trono sostiene cetro largo en la derecha y escudo con águila bicéfala en la izquierda",
        "simbolos":    ["cetro largo", "escudo con águila bicéfala", "corona real", "trono ornamentado"],
        "verificado":  False,
    },
    "AM-04": {  # El Emperador
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne"],
        "figura_mira": "derecha",
        "gesto":       "sentado de perfil, pierna cruzada forma un 4; sostiene cetro con cruz en la punta; barba azul",
        "simbolos":    ["cetro con cruz", "escudo con águila", "pierna en cuatro", "barba azul", "corona"],
        "verificado":  False,
    },
    "AM-05": {  # El Papa
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne"],
        "figura_mira": "frente",
        "gesto":       "bendice levantando dos dedos; sostiene triple báculo; dos acólitos se inclinan ante él",
        "simbolos":    ["triple báculo", "tiara triple", "mano bendiciente", "dos acólitos arrodillados", "columnas"],
        "verificado":  False,
    },
    "AM-06": {  # Los Enamorados
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne", "verde"],
        "figura_mira": "frente",
        "gesto":       "joven en encrucijada entre dos mujeres; Cupido apunta su flecha desde nube en lo alto",
        "simbolos":    ["Cupido con flecha", "dos mujeres", "sol con rostro", "nube", "corona floral"],
        "verificado":  False,
    },
    "AM-07": {  # El Carro
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne"],
        "figura_mira": "frente",
        "gesto":       "príncipe armado avanza en carro sin ruedas; dos esfinges (roja y azul) tiran en sentidos opuestos",
        "simbolos":    ["carro sin ruedas", "dos esfinges opuestas", "yelmo coronado con estrella", "hombreras con rostros", "cetro"],
        "verificado":  False,
    },
    "AM-08": {  # La Justicia
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne"],
        "figura_mira": "frente",
        "gesto":       "sentada en trono sostiene balanza en mano izquierda y espada recta apuntando arriba en la derecha",
        "simbolos":    ["balanza", "espada recta", "corona real", "trono", "columnas rojas"],
        "verificado":  False,
    },
    "AM-09": {  # El Ermitaño
        "colores":     ["azul oscuro", "rojo", "amarillo claro", "carne"],
        "figura_mira": "izquierda abajo",
        "gesto":       "anciano encapuchado camina de perfil con bastón alto; sostiene linterna encendida hacia adelante",
        "simbolos":    ["linterna encendida", "bastón largo", "capucha", "manto azul", "suelo nevado o vacío"],
        "verificado":  False,
    },
    "AM-10": {  # La Rueda de Fortuna
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne", "negro"],
        "figura_mira": "ninguna figura central",
        "gesto":       "rueda mecánica gira; figura sube por la derecha, figura cae por la izquierda; esfinge con espada en la cima",
        "simbolos":    ["rueda giratoria", "Anubis subiendo", "figura cayendo", "esfinge con espada en cima", "manivela"],
        "verificado":  False,
    },
    "AM-11": {  # La Fuerza
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne", "verde"],
        "figura_mira": "izquierda",
        "gesto":       "mujer con sombrero en forma de infinito abre/cierra suavemente las fauces del león con ambas manos, sin violencia",
        "simbolos":    ["sombrero infinito (∞)", "león", "guirnalda de flores", "cadena floral"],
        "verificado":  False,
    },
    "AM-12": {  # El Colgado
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne"],
        "figura_mira": "frente (boca abajo)",
        "gesto":       "joven cuelga boca abajo de un pie desde viga en T; piernas forman triángulo; brazos ocultos tras la espalda",
        "simbolos":    ["viga en T", "pie atado", "triángulo de piernas", "árboles podados", "brazos ocultos"],
        "verificado":  False,
    },
    "AM-13": {  # El Arcano XIII
        "colores":     ["negro", "rojo", "amarillo claro", "azul claro", "carne"],
        "figura_mira": "derecha",
        "gesto":       "esqueleto desnudo siega horizontalmente con guadaña; de la tierra brotan cabezas, manos y pies; sin nombre escrito",
        "simbolos":    ["esqueleto", "guadaña horizontal", "cabezas brotando de la tierra", "manos y pies cortados", "letras YHVH en el cráneo"],
        "verificado":  False,
    },
    "AM-14": {  # La Templanza
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne", "verde"],
        "figura_mira": "ligeramente derecha",
        "gesto":       "ángel andrógino vierte líquido entre dos copas sin derramar; un pie en tierra y el otro en el agua",
        "simbolos":    ["dos copas", "líquido vertido sin derrames", "alas multicolores", "flor en la frente", "pie en el agua"],
        "verificado":  False,
    },
    "AM-15": {  # El Diablo — verificado: cuerpo azul claro confirmado
        "colores":     ["azul claro", "negro", "rojo", "amarillo claro", "carne"],
        "figura_mira": "frente",
        "gesto":       "demonio de cuerpo azul claro con cuernos, alas de murciélago y pezuñas; yergue antorcha encendida desde pedestal; cara visible también en el ombligo; pareja humana encadenada por el cuello a sus pies",
        "simbolos":    ["cuerpo azul del demonio", "antorcha encendida", "cadenas en los cuellos", "pareja encadenada", "alas de murciélago", "cara en el ombligo", "pezuñas"],
        "verificado":  True,
    },
    "AM-16": {  # La Torre
        "colores":     ["rojo", "azul claro", "amarillo claro", "negro", "verde", "carne"],
        "figura_mira": "ninguna (acción pura)",
        "gesto":       "rayo golpea la corona de la torre haciéndola volar; dos figuras caen de cabeza desde las almenas",
        "simbolos":    ["rayo del cielo", "corona volando", "dos figuras cayendo de cabeza", "gotas ardientes", "abertura triangular en el muro"],
        "verificado":  False,
    },
    "AM-17": {  # La Estrella
        "colores":     ["azul claro", "rojo", "amarillo claro", "verde", "carne"],
        "figura_mira": "abajo",
        "gesto":       "mujer desnuda arrodillada vierte agua de dos jarras: una al estanque y otra a la tierra; ocho estrellas arriba",
        "simbolos":    ["ocho estrellas (una grande, siete pequeñas)", "dos jarras", "agua fluyendo", "árbol con pájaro", "estanque", "desnudez"],
        "verificado":  False,
    },
    "AM-18": {  # La Luna
        "colores":     ["azul claro", "azul oscuro", "rojo", "amarillo claro", "verde", "carne"],
        "figura_mira": "luna mira abajo; cangrejo mira arriba",
        "gesto":       "luna llena con rostro humano derrama gotas; cangrejo emerge del agua; dos perros aúllan ante las torres",
        "simbolos":    ["luna con rostro", "dos torres flanqueando", "cangrejo emergiendo del agua", "dos perros aullando", "gotas cayendo", "camino entre torres"],
        "verificado":  False,
    },
    "AM-19": {  # El Sol
        "colores":     ["amarillo claro", "rojo", "azul claro", "carne"],
        "figura_mira": "frente",
        "gesto":       "dos niños desnudos tomados de la mano ante muro semicircular; sol radiante con rostro sonriente los ilumina",
        "simbolos":    ["sol con rostro sonriente", "dos niños desnudos", "muro semicircular de piedra", "gotas de luz cayendo"],
        "verificado":  False,
    },
    "AM-20": {  # El Juicio
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne", "negro"],
        "figura_mira": "arriba (hacia el ángel)",
        "gesto":       "ángel toca trompeta desde nube; tres figuras resucitan de ataúdes abiertos con brazos extendidos al cielo",
        "simbolos":    ["ángel trompetero", "tres ataúdes abiertos", "tres resucitados", "nube", "bandera con cruz"],
        "verificado":  False,
    },
    "AM-21": {  # El Mundo
        "colores":     ["rojo", "azul claro", "amarillo claro", "verde", "carne", "violeta"],
        "figura_mira": "ligeramente derecha",
        "gesto":       "figura andrógina danza desnuda dentro de guirnalda ovalada; cuatro figuras en los ángulos: ángel, águila, león, buey",
        "simbolos":    ["guirnalda ovalada", "figura danzante", "ángel (arriba izquierda)", "águila (arriba derecha)", "león (abajo derecha)", "buey (abajo izquierda)", "dos varas"],
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
    "ME-BAS-11": {  # Sota de Bastos
        "colores":     ["rojo", "azul claro", "carne"],
        "figura_mira": "derecha",
        "gesto":       "joven de pie sostiene bastón largo con brío; postura activa hacia la derecha",
        "simbolos":    ["bastón largo", "calzas de colores", "sombrero con pluma", "botas"],
        "verificado":  False,
    },
    "ME-BAS-12": {  # Caballero de Bastos
        "colores":     ["rojo", "azul claro", "amarillo claro", "carne"],
        "figura_mira": "derecha (galope)",
        "gesto":       "jinete al galope con bastón en alto; caballo con patas delanteras elevadas",
        "simbolos":    ["caballo al galope", "bastón en alto", "yelmo con pluma", "armadura parcial"],
        "verificado":  False,
    },
    "ME-BAS-13": {  # Reina de Bastos
        "colores":     ["rojo", "azul claro", "amarillo claro"],
        "figura_mira": "derecha",
        "gesto":       "sentada sostiene bastón corto con autoridad; postura erguida en trono ornamentado",
        "simbolos":    ["bastón corto", "trono ornamentado", "corona floral", "manto rojo"],
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
    "ME-COP-11": {  # Sota de Copas
        "colores":     ["amarillo claro", "rojo", "azul claro", "carne"],
        "figura_mira": "izquierda",
        "gesto":       "joven mira hacia la izquierda contemplando la copa dorada que sostiene con cuidado",
        "simbolos":    ["copa dorada", "sombrero de perfil", "capa decorada", "postura contemplativa"],
        "verificado":  False,
    },
    "ME-COP-12": {  # Caballero de Copas
        "colores":     ["amarillo claro", "rojo", "azul claro", "carne"],
        "figura_mira": "derecha",
        "gesto":       "jinete avanza llevando la copa dorada como si fuera el Grial; paso sereno",
        "simbolos":    ["caballo al paso", "copa dorada elevada", "yelmo emplumado", "armadura"],
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
    "ME-ESP-12": {  # Caballero de Espadas
        "colores":     ["rojo", "azul claro", "negro", "carne"],
        "figura_mira": "derecha (galope)",
        "gesto":       "jinete al galope con espada en alto en acción de corte; caballo en plena carrera",
        "simbolos":    ["caballo al galope", "espada en alto", "yelmo emplumado", "armadura completa"],
        "verificado":  False,
    },
    "ME-ESP-13": {  # Reina de Espadas
        "colores":     ["rojo", "azul claro", "negro", "carne"],
        "figura_mira": "derecha",
        "gesto":       "sentada sostiene espada recta apuntando al cielo; mirada directa y penetrante",
        "simbolos":    ["espada recta al cielo", "trono", "corona", "manto"],
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
    "ME-ORO-11": {  # Sota de Oros
        "colores":     ["amarillo claro", "azul claro", "rojo"],
        "figura_mira": "frente abajo",
        "gesto":       "joven con un pie a cada lado contempla el oro que flota ante él; postura de asombro",
        "simbolos":    ["oro flotante", "postura contemplativa", "dos pies en tierra", "sombrero"],
        "verificado":  False,
    },
    "ME-ORO-12": {  # Caballero de Oros
        "colores":     ["amarillo claro", "rojo", "azul claro", "verde"],
        "figura_mira": "derecha (paso)",
        "gesto":       "jinete al paso sostiene moneda de oro espiritualizada; movimiento tranquilo",
        "simbolos":    ["caballo al paso", "moneda dorada elevada", "yelmo", "vegetación"],
        "verificado":  False,
    },
    "ME-ORO-13": {  # Reina de Oros
        "colores":     ["rojo", "azul claro", "amarillo claro"],
        "figura_mira": "derecha",
        "gesto":       "sentada sostiene moneda con gesto de quien conoce su valor real",
        "simbolos":    ["moneda dorada", "trono ornamentado", "corona", "manto rojo"],
        "verificado":  False,
    },
    "ME-ORO-14": {  # Rey de Oros
        "colores":     ["amarillo claro", "rojo", "azul claro"],
        "figura_mira": "derecha",
        "gesto":       "entronado sostiene moneda y cetro; presencia material plena y estable",
        "simbolos":    ["moneda dorada", "cetro", "trono", "corona imperial", "manto"],
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
