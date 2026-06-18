"""
Tarot Terapéutico — Tarot de Marsella, método Jodorowsky-Camoin.

Marco filosófico: Alejandro Jodorowsky, "La Vía del Tarot" (con Marianne Costa).
  — El Tarot no predice: lee qué fuerza arquetípica está activa ahora.
  — Las cartas NO se invierten: se barajan girando hacia la derecha (Jodorowsky).
  — Posición = marco energético. Carta = contenido. Juntas = el mensaje.
  — El significado surge del diálogo entre cartas, no de lecturas aisladas.
"""

import random
from dataclasses import dataclass, field
from typing import Optional


# ── Imágenes ──────────────────────────────────────────────────────────────────

_PALO_LETRA = {"bastos": "b", "copas": "c", "oros": "d", "espadas": "e"}


def _imagen_mayor(numero: int) -> str:
    if numero == 0:
        return "img/tarot/a22.jpg"
    return f"img/tarot/a{numero:02d}.jpg"


def _imagen_menor(palo: str, num: int) -> str:
    letra = _PALO_LETRA.get(palo, "b")
    return f"img/tarot/{letra}{num:02d}.jpg"


# ── Arcanos Mayores ───────────────────────────────────────────────────────────
# Orden Marsella: VIII=Justicia, XI=Fuerza (no intercambiado como en RWS).
# El Arcano XIII no tiene nombre en el Tarot de Marsella original.

ARCANOS_MAYORES = [
    {
        "id": 0, "nombre": "El Loco", "palabra_clave": "libertad absoluta",
        "arquetipo": "El inicio sin condición",
        "visual": {
            "colores": ["rojo", "verde", "carne", "azul claro", "amarillo claro"],
            "figura_mira": "derecha",
            "gesto": "camina alegremente con bastón y bolsa al hombro sin ver el abismo; un perro le muerde la ropa",
            "simbolos": ["bastón con bolsa", "perro mordiéndo la ropa", "precipicio al borde", "flores en el bastón"],
        },
    },
    {
        "id": 1, "nombre": "El Mago", "palabra_clave": "voluntad consciente",
        "arquetipo": "La conciencia que actúa",
        "visual": {
            "colores": ["rojo", "amarillo claro", "carne", "azul claro"],
            "figura_mira": "derecha",
            "gesto": "señala al cielo con varita mientras la otra mano toca objetos sobre la mesa",
            "simbolos": ["mesa con objetos", "varita", "copa", "cuchillo", "moneda", "dado", "sombrero de borde infinito"],
        },
    },
    {
        "id": 2, "nombre": "La Papisa", "palabra_clave": "sabiduría interior",
        "arquetipo": "El saber que no habla",
        "visual": {
            "colores": ["azul oscuro", "rojo", "amarillo claro", "blanco"],
            "figura_mira": "frente",
            "gesto": "sostiene libro cerrado sobre el regazo; velo blanco cae detrás; boca sellada",
            "simbolos": ["libro cerrado", "tiara triple", "velo blanco", "columnas", "manto azul"],
        },
    },
    {
        "id": 3, "nombre": "La Emperatriz", "palabra_clave": "creación fértil",
        "arquetipo": "La madre que genera",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "verde", "carne"],
            "figura_mira": "derecha",
            "gesto": "sentada en trono sostiene cetro largo en la derecha y escudo con águila bicéfala en la izquierda",
            "simbolos": ["cetro largo", "escudo con águila bicéfala", "corona real", "trono ornamentado"],
        },
    },
    {
        "id": 4, "nombre": "El Emperador", "palabra_clave": "estructura y orden",
        "arquetipo": "El padre que sostiene",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne"],
            "figura_mira": "derecha",
            "gesto": "sentado de perfil, pierna cruzada forma un 4; sostiene cetro con cruz en la punta; barba azul",
            "simbolos": ["cetro con cruz", "escudo con águila", "pierna en cuatro", "barba azul", "corona"],
        },
    },
    {
        "id": 5, "nombre": "El Papa", "palabra_clave": "transmisión sagrada",
        "arquetipo": "El puente entre mundos",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne"],
            "figura_mira": "frente",
            "gesto": "bendice levantando dos dedos; sostiene triple báculo; dos acólitos se inclinan ante él",
            "simbolos": ["triple báculo", "tiara triple", "mano bendiciente", "dos acólitos arrodillados", "columnas"],
        },
    },
    {
        "id": 6, "nombre": "Los Enamorados", "palabra_clave": "elección vital",
        "arquetipo": "La encrucijada del deseo",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne", "verde"],
            "figura_mira": "frente",
            "gesto": "joven en encrucijada entre dos mujeres; Cupido apunta su flecha desde nube en lo alto",
            "simbolos": ["Cupido con flecha", "dos mujeres", "sol con rostro", "nube", "corona floral"],
        },
    },
    {
        "id": 7, "nombre": "El Carro", "palabra_clave": "voluntad victoriosa",
        "arquetipo": "El dominio del impulso",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne"],
            "figura_mira": "frente",
            "gesto": "príncipe armado avanza en carro sin ruedas; dos esfinges (roja y azul) tiran en sentidos opuestos",
            "simbolos": ["carro sin ruedas", "dos esfinges opuestas", "yelmo coronado con estrella", "hombreras con rostros", "cetro"],
        },
    },
    {
        "id": 8, "nombre": "La Justicia", "palabra_clave": "verdad precisa",
        "arquetipo": "El equilibrio que corta",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne"],
            "figura_mira": "frente",
            "gesto": "sentada en trono sostiene balanza en mano izquierda y espada recta apuntando arriba en la derecha",
            "simbolos": ["balanza", "espada recta", "corona real", "trono", "columnas rojas"],
        },
    },
    {
        "id": 9, "nombre": "El Ermitaño", "palabra_clave": "búsqueda interior",
        "arquetipo": "La luz que ilumina desde adentro",
        "visual": {
            "colores": ["azul oscuro", "rojo", "amarillo claro", "carne"],
            "figura_mira": "izquierda abajo",
            "gesto": "anciano encapuchado camina de perfil con bastón alto; sostiene linterna encendida hacia adelante",
            "simbolos": ["linterna encendida", "bastón largo", "capucha", "manto azul", "suelo nevado o vacío"],
        },
    },
    {
        "id": 10, "nombre": "La Rueda de Fortuna", "palabra_clave": "ciclo en movimiento",
        "arquetipo": "El ritmo inevitable del cambio",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne", "negro"],
            "figura_mira": "ninguna figura central",
            "gesto": "rueda mecánica gira; figura sube por la derecha, figura cae por la izquierda; esfinge con espada en la cima",
            "simbolos": ["rueda giratoria", "Anubis subiendo", "figura cayendo", "esfinge con espada en cima", "manivela"],
        },
    },
    {
        "id": 11, "nombre": "La Fuerza", "palabra_clave": "dominio del instinto",
        "arquetipo": "El amor que doma la bestia",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne", "verde"],
            "figura_mira": "izquierda",
            "gesto": "mujer con sombrero en forma de infinito abre/cierra suavemente las fauces del león con ambas manos, sin violencia",
            "simbolos": ["sombrero infinito (∞)", "león", "guirnalda de flores", "cadena floral"],
        },
    },
    {
        "id": 12, "nombre": "El Colgado", "palabra_clave": "entrega y perspectiva",
        "arquetipo": "La inversión que revela",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne"],
            "figura_mira": "frente (boca abajo)",
            "gesto": "joven cuelga boca abajo de un pie desde viga en T; piernas forman triángulo; brazos ocultos tras la espalda",
            "simbolos": ["viga en T", "pie atado", "triángulo de piernas", "árboles podados", "brazos ocultos"],
        },
    },
    {
        "id": 13, "nombre": "El Arcano XIII", "palabra_clave": "transformación radical",
        "arquetipo": "El fin que abre",
        "visual": {
            "colores": ["negro", "rojo", "amarillo claro", "azul claro", "carne"],
            "figura_mira": "derecha",
            "gesto": "esqueleto desnudo siega horizontalmente con guadaña; de la tierra brotan cabezas, manos y pies; sin nombre escrito",
            "simbolos": ["esqueleto", "guadaña horizontal", "cabezas brotando de la tierra", "manos y pies cortados", "letras YHVH en el cráneo"],
        },
    },
    {
        "id": 14, "nombre": "La Templanza", "palabra_clave": "alquimia y flujo",
        "arquetipo": "La mezcla que transforma",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne", "verde"],
            "figura_mira": "ligeramente derecha",
            "gesto": "ángel andrógino vierte líquido entre dos copas sin derramar; un pie en tierra y el otro en el agua",
            "simbolos": ["dos copas", "líquido vertido sin derrames", "alas multicolores", "flor en la frente", "pie en el agua"],
        },
    },
    {
        "id": 15, "nombre": "El Diablo", "palabra_clave": "sombra encadenada",
        "arquetipo": "El apego que ilusiona",
        "visual": {
            "colores": ["negro", "rojo", "amarillo claro", "carne", "azul claro"],
            "figura_mira": "frente",
            "gesto": "demonio con alas de murciélago yergue antorcha en alto desde pedestal; pareja humana encadenada a sus pies",
            "simbolos": ["antorcha encendida", "cadenas en los cuellos", "pareja encadenada", "alas de murciélago", "cuernos", "cara en el ombligo", "pezuñas"],
        },
    },
    {
        "id": 16, "nombre": "La Torre", "palabra_clave": "derrumbe liberador",
        "arquetipo": "La verdad que destruye la mentira",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "negro", "verde", "carne"],
            "figura_mira": "ninguna (acción pura)",
            "gesto": "rayo golpea la corona de la torre haciéndola volar; dos figuras caen de cabeza desde las almenas",
            "simbolos": ["rayo del cielo", "corona volando", "dos figuras cayendo de cabeza", "gotas ardientes", "abertura triangular en el muro"],
        },
    },
    {
        "id": 17, "nombre": "La Estrella", "palabra_clave": "esperanza desnuda",
        "arquetipo": "La fe sin certeza",
        "visual": {
            "colores": ["azul claro", "rojo", "amarillo claro", "verde", "carne"],
            "figura_mira": "abajo",
            "gesto": "mujer desnuda arrodillada vierte agua de dos jarras: una al estanque y otra a la tierra; ocho estrellas arriba",
            "simbolos": ["ocho estrellas (una grande, siete pequeñas)", "dos jarras", "agua fluyendo", "árbol con pájaro", "estanque", "desnudez"],
        },
    },
    {
        "id": 18, "nombre": "La Luna", "palabra_clave": "inconsciente profundo",
        "arquetipo": "El umbral de lo que aún no es",
        "visual": {
            "colores": ["azul claro", "azul oscuro", "rojo", "amarillo claro", "verde", "carne"],
            "figura_mira": "luna mira abajo; cangrejo mira arriba",
            "gesto": "luna llena con rostro humano derrama gotas; cangrejo emerge del agua; dos perros aúllan ante las torres",
            "simbolos": ["luna con rostro", "dos torres flanqueando", "cangrejo emergiendo del agua", "dos perros aullando", "gotas cayendo", "camino entre torres"],
        },
    },
    {
        "id": 19, "nombre": "El Sol", "palabra_clave": "claridad y alegría",
        "arquetipo": "La conciencia plena",
        "visual": {
            "colores": ["amarillo claro", "rojo", "azul claro", "carne"],
            "figura_mira": "frente",
            "gesto": "dos niños desnudos tomados de la mano ante muro semicircular; sol radiante con rostro sonriente los ilumina",
            "simbolos": ["sol con rostro sonriente", "dos niños desnudos", "muro semicircular de piedra", "gotas de luz cayendo"],
        },
    },
    {
        "id": 20, "nombre": "El Juicio", "palabra_clave": "llamado al despertar",
        "arquetipo": "La resurrección desde adentro",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "carne", "negro"],
            "figura_mira": "arriba (hacia el ángel)",
            "gesto": "ángel toca trompeta desde nube; tres figuras resucitan de ataúdes abiertos con brazos extendidos al cielo",
            "simbolos": ["ángel trompetero", "tres ataúdes abiertos", "tres resucitados", "nube", "bandera con cruz"],
        },
    },
    {
        "id": 21, "nombre": "El Mundo", "palabra_clave": "integración total",
        "arquetipo": "La danza del ser completo",
        "visual": {
            "colores": ["rojo", "azul claro", "amarillo claro", "verde", "carne", "violeta"],
            "figura_mira": "ligeramente derecha",
            "gesto": "figura andrógina danza desnuda dentro de guirnalda ovalada; cuatro figuras en los ángulos: ángel, águila, león, buey",
            "simbolos": ["guirnalda ovalada", "figura danzante", "ángel (arriba izquierda)", "águila (arriba derecha)", "león (abajo derecha)", "buey (abajo izquierda)", "dos varas"],
        },
    },
]

# ── Arcanos Menores ───────────────────────────────────────────────────────────
# Elementos según Jodorowsky: Bastos=Fuego/libido, Copas=Agua/emoción,
# Espadas=Aire/mente, Oros=Tierra/cuerpo.
# Visual de los palos en el Tarot de Marsella: los naipes numéricos (1-10)
# no tienen escenas figurativas — muestran el símbolo del palo en disposición
# geométrica. Las figuras (Sota/Caballero/Reina/Rey) sí tienen personajes.

PALOS_MENORES = [
    {
        "palo": "bastos", "elemento": "fuego",
        "esencia": "el impulso creador, la energía vital, la libido que construye",
        "colores_palo": ["rojo", "azul claro", "negro"],
        "visual_numerales": "bastos rojos con extremos negros dispuestos simétricamente; ornamentos vegetales azules entre ellos; la energía crece de As a Diez",
    },
    {
        "palo": "copas", "elemento": "agua",
        "esencia": "el mundo emocional, el amor, lo que fluye y lo que se evita sentir",
        "colores_palo": ["azul claro", "rojo", "carne"],
        "visual_numerales": "copas azules con detalles rojos, algunas con tapas; el As parece una catedral gótica; ornamentos florales entre las copas",
    },
    {
        "palo": "espadas", "elemento": "aire",
        "esencia": "la mente, la palabra, el corte, el conflicto que revela la verdad",
        "colores_palo": ["negro", "rojo", "azul claro"],
        "visual_numerales": "espadas negras con guarda roja y azul en disposición oval; se cruzan o entrelazan según el número; el diseño se vuelve más denso al crecer",
    },
    {
        "palo": "oros", "elemento": "tierra",
        "esencia": "el cuerpo, los recursos, la materia, lo que se tiene o se carece",
        "colores_palo": ["amarillo claro", "rojo", "verde"],
        "visual_numerales": "círculos dorados sin número impreso (único palo sin numeración visible); disposición geométrica simétrica; los Oros son siempre redondos y vacíos",
    },
]

# Figuras: la dirección varía por palo y refleja la cualidad del palo.
# Bastos (activo): miran a la derecha.
# Copas (receptivo): Sota y Reina miran a la izquierda (receptivas).
# Espadas: miran a la derecha (corte activo).
# Oros: Sota de Oros mira al frente/abajo (los Oros no tienen número, la Sota los contempla).

FIGURAS_VISUAL = {
    "sota_bastos":      {"mira": "derecha",        "colores": ["rojo", "azul claro", "carne"], "gesto": "joven de pie sostiene bastón con brío"},
    "caballero_bastos": {"mira": "derecha (galope)","colores": ["rojo", "azul claro", "amarillo claro", "carne"], "gesto": "jinete al galope con bastón en alto"},
    "reina_bastos":     {"mira": "derecha",        "colores": ["rojo", "azul claro", "amarillo claro"], "gesto": "sentada sostiene bastón corto con autoridad"},
    "rey_bastos":       {"mira": "derecha",        "colores": ["rojo", "azul claro", "amarillo claro"], "gesto": "entronado sostiene bastón largo y cetro"},
    "sota_copas":       {"mira": "izquierda",      "colores": ["azul claro", "rojo", "carne"], "gesto": "joven contempla la copa que sostiene con cuidado"},
    "caballero_copas":  {"mira": "derecha",        "colores": ["azul claro", "rojo", "carne", "amarillo claro"], "gesto": "jinete lleva la copa como si fuera el Grial"},
    "reina_copas":      {"mira": "izquierda",      "colores": ["azul claro", "rojo", "amarillo claro"], "gesto": "sentada sostiene copa con tapa; mirada interior"},
    "rey_copas":        {"mira": "derecha",        "colores": ["azul claro", "rojo", "amarillo claro"], "gesto": "entronado sostiene copa y cetro; expresión serena"},
    "sota_espadas":     {"mira": "derecha",        "colores": ["negro", "rojo", "azul claro", "carne"], "gesto": "joven sostiene espada con ambas manos en posición activa"},
    "caballero_espadas":{"mira": "derecha (galope)","colores": ["rojo", "azul claro", "negro", "carne"], "gesto": "jinete al galope con espada en alto en acción de corte"},
    "reina_espadas":    {"mira": "derecha",        "colores": ["rojo", "azul claro", "negro", "carne"], "gesto": "sentada sostiene espada recta apuntando al cielo"},
    "rey_espadas":      {"mira": "derecha",        "colores": ["rojo", "azul claro", "negro"], "gesto": "entronado con espada larga; mirada penetrante"},
    "sota_oros":        {"mira": "frente abajo",   "colores": ["amarillo claro", "azul claro", "rojo"], "gesto": "joven con un pie a cada lado contempla el oro que flota ante él"},
    "caballero_oros":   {"mira": "derecha (paso)", "colores": ["amarillo claro", "rojo", "azul claro", "verde"], "gesto": "jinete al paso sostiene moneda de oro espiritualizada"},
    "reina_oros":       {"mira": "derecha",        "colores": ["rojo", "azul claro", "amarillo claro"], "gesto": "sentada sostiene moneda con gesto de quien conoce su valor"},
    "rey_oros":         {"mira": "derecha",        "colores": ["amarillo claro", "rojo", "azul claro"], "gesto": "entronado sostiene moneda y cetro; presencia material plena"},
}

NUMEROS_MENORES = [
    {"num": 1,  "nombre": "As",        "significado": "potencial absoluto, la semilla antes de manifestarse"},
    {"num": 2,  "nombre": "Dos",       "significado": "encuentro, espejo, la primera relación"},
    {"num": 3,  "nombre": "Tres",      "significado": "creación por síntesis, la trinidad en acción"},
    {"num": 4,  "nombre": "Cuatro",    "significado": "manifestación, estructura, la base sólida"},
    {"num": 5,  "nombre": "Cinco",     "significado": "crisis transformadora, el punto de quiebre necesario"},
    {"num": 6,  "nombre": "Seis",      "significado": "amor, armonía, la resolución que integra"},
    {"num": 7,  "nombre": "Siete",     "significado": "el viaje interior, lo sagrado, la pregunta sin respuesta fácil"},
    {"num": 8,  "nombre": "Ocho",      "significado": "movimiento justo, karma en acción, el ciclo que se cumple"},
    {"num": 9,  "nombre": "Nueve",     "significado": "culminación solitaria, sabiduría al borde del umbral"},
    {"num": 10, "nombre": "Diez",      "significado": "exceso, fin de ciclo, lo que debe soltar para que nazca algo nuevo"},
    {"num": 11, "nombre": "Sota",      "significado": "el aprendiz, lo que aún no ha encontrado su forma"},
    {"num": 12, "nombre": "Caballero", "significado": "la energía en movimiento hacia su destino"},
    {"num": 13, "nombre": "Reina",     "significado": "la autoridad interior, el dominio receptivo y maduro"},
    {"num": 14, "nombre": "Rey",       "significado": "la realización del palo, el maestro de ese elemento"},
]


def _construir_mazo_completo() -> list[dict]:
    mazo = []
    for arcano in ARCANOS_MAYORES:
        mazo.append({
            "id": f"AM-{arcano['id']:02d}",
            "nombre": arcano["nombre"],
            "tipo": "mayor",
            "palo": None,
            "elemento": None,
            "numero": arcano["id"],
            "palabra_clave": arcano["palabra_clave"],
            "arquetipo": arcano["arquetipo"],
            "imagen": _imagen_mayor(arcano["id"]),
            "visual": arcano["visual"],
        })
    for palo_info in PALOS_MENORES:
        for num_info in NUMEROS_MENORES:
            nombre_carta = f"{num_info['nombre']} de {palo_info['palo'].capitalize()}"
            # Visual para figuras (cartas con personaje)
            if num_info["num"] >= 11:
                figura_key = f"{num_info['nombre'].lower()}_{palo_info['palo']}"
                v = FIGURAS_VISUAL.get(figura_key, {})
                visual = {
                    "colores": v.get("colores", palo_info["colores_palo"]),
                    "figura_mira": v.get("mira", "derecha"),
                    "gesto": v.get("gesto", ""),
                    "simbolos": [palo_info["palo"], "figura entronada o de pie"],
                }
            else:
                # Naipes numéricos: sin figuras, solo disposición de símbolos
                visual = {
                    "colores": palo_info["colores_palo"],
                    "figura_mira": "sin figura",
                    "gesto": f"{num_info['nombre']} {palo_info['palo']} en disposición geométrica",
                    "simbolos": [palo_info["palo"], f"número {num_info['num']}"],
                }
            mazo.append({
                "id": f"ME-{palo_info['palo'][:3].upper()}-{num_info['num']:02d}",
                "nombre": nombre_carta,
                "tipo": "menor",
                "palo": palo_info["palo"],
                "elemento": palo_info["elemento"],
                "numero": num_info["num"],
                "palabra_clave": num_info["significado"],
                "arquetipo": palo_info["esencia"],
                "imagen": _imagen_menor(palo_info["palo"], num_info["num"]),
                "visual": visual,
            })
    return mazo


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass
class CartaTarot:
    id: str
    nombre: str
    tipo: str
    palo: Optional[str]
    elemento: Optional[str]
    numero: int
    palabra_clave: str
    arquetipo: str
    imagen: str = ""
    posicion: str = ""
    visual: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "palo": self.palo,
            "elemento": self.elemento,
            "numero": self.numero,
            "palabra_clave": self.palabra_clave,
            "arquetipo": self.arquetipo,
            "imagen": self.imagen,
            "posicion": self.posicion,
            "visual": self.visual,
        }


@dataclass
class TiradaTarot:
    tipo_tirada: str
    cartas: list[CartaTarot] = field(default_factory=list)
    pregunta: str = ""

    def to_dict(self) -> dict:
        return {
            "tipo_tirada": self.tipo_tirada,
            "pregunta": self.pregunta,
            "cartas": [c.to_dict() for c in self.cartas],
        }


# ── TarotService ──────────────────────────────────────────────────────────────

class TarotService:
    """
    Barajado, selección de tiradas y preparación de datos.

    Tiradas disponibles (Jodorowsky, "La Vía del Tarot"):
    — un_arcano:       1 carta · espejo directo
    — fuerza_flaqueza: 2 cartas · Fuerza y Flaqueza
    — el_conflicto:    2 cartas · El Conflicto
    — tres_cartas:     3 cartas · Raíz–Tallo–Flor
    — la_duda:         4 cartas · La Duda
    — la_liberacion:   5 cartas · La Liberación
    — el_heroe_5:      5 cartas · El Héroe
    — el_mundo:        5 cartas · El Mundo
    — cruz_normal:     5 cartas · La Cruz
    — yo_realizado:    10 cartas · El Yo Realizado
    — viaje_heroe:     12 arcanos mayores · Viaje del Héroe
    """

    POSICIONES_FUERZA_FLAQUEZA = ["fuerza", "flaqueza"]

    # El Conflicto: situacion normal + tension cruzada encima (crossing pair)
    POSICIONES_CONFLICTO = ["situacion", "tension"]

    POSICIONES_TRES = ["raiz", "tallo", "flor"]

    # La Duda: quién soy + las dos caras de la duda + la clave
    POSICIONES_DUDA = ["duda_a", "consultante_d", "duda_b", "clave_d"]

    # La Liberación: bloqueo → medio → acción → transformación → destino
    POSICIONES_LIBERACION = ["bloqueo", "medio", "accion", "transformacion", "destino"]

    # El Héroe (5 cartas): partida → meta, con dos obstáculos (leídos en par) y clave
    POSICIONES_HEROE_5 = ["partida", "obstaculo_a", "meta", "obstaculo_b", "clave_h"]

    # El Mundo: inspirado en el Arcano XXI — esencia central + 4 dimensiones del ser
    POSICIONES_MUNDO = ["esencia", "intelectual", "emocional", "sexual_creativo", "material"]

    POSICIONES_CRUZ_NORMAL = ["presente", "sombra", "pasado", "camino", "fundamento"]

    # Tarot del Yo Realizado (Jodorowsky, "La Vía del Tarot", Quinta parte)
    POSICIONES_YO_REALIZADO = [
        "protagonista", "mediador", "antagonista",
        "cometa_a", "secreto", "asteroide_a",
        "cometa_b", "resultado_a", "asteroide_b",
        "resultado_b",
    ]

    POSICIONES_HEROE = [
        "mundo_ordinario", "llamado", "rechazo", "mentor",
        "cruce_umbral", "pruebas", "caverna", "prueba_suprema",
        "recompensa", "camino_regreso", "resurreccion", "elixir",
    ]

    NOMBRES_POSICIONES = {
        # Una carta
        "unica":             "Carta espejo",
        # Fuerza y Flaqueza
        "fuerza":            "Tu recurso — lo que ya tienes",
        "flaqueza":          "Tu sombra — lo que aún no integraste",
        # El Conflicto
        "situacion":         "La situación o deseo",
        "tension":           "La tensión que la atraviesa",
        # Tres cartas
        "raiz":              "Raíz — causa profunda inconsciente",
        "tallo":             "Tallo — presente vivido",
        "flor":              "Flor — potencial que puede nacer",
        # La Duda
        "consultante_d":     "Tú en este momento",
        "duda_a":            "Una cara de la duda",
        "duda_b":            "La otra cara de la duda",
        "clave_d":           "La clave para decidir",
        # La Liberación
        "bloqueo":           "Qué me impide ser yo",
        "medio":             "Cómo liberarme",
        "accion":            "Para qué acción concreta",
        "transformacion":    "Hacia qué transformación",
        "destino":           "Mi objetivo real",
        # El Héroe (5 cartas)
        "partida":           "De dónde parto",
        "meta":              "Hacia dónde voy",
        "obstaculo_a":       "Obstáculo — cara exterior",
        "obstaculo_b":       "Obstáculo — cara interior",
        "clave_h":           "El aliado o clave",
        # El Mundo
        "esencia":           "Tu esencia — quién eres",
        "intelectual":       "Tu vida intelectual",
        "emocional":         "Tu vida emocional",
        "sexual_creativo":   "Tu energía creativa y vital",
        "material":          "Tu vida material",
        # Cruz de 5
        "presente":          "Presente",
        "sombra":            "Sombra — la cara oculta del presente",
        "pasado":            "Pasado reciente",
        "camino":            "Camino abierto",
        "fundamento":        "Fundamento inconsciente",
        # Tarot del Yo Realizado
        "protagonista":      "Protagonista — cómo me concibo",
        "antagonista":       "Antagonista — lo que rechazo de mí",
        "mediador":          "Mediador — lo que pasa entre ambos",
        "cometa_a":          "Cometa A — lo que me nutre",
        "cometa_b":          "Cometa B — lo que me expande",
        "asteroide_a":       "Asteroide A — lo que me frena",
        "asteroide_b":       "Asteroide B — lo que me perjudica",
        "resultado_a":       "Resultado A — lo que emerge",
        "resultado_b":       "Resultado B — la personalidad que nace",
        "secreto":           "El Secreto — mi lugar más íntimo",
        # Viaje del Héroe
        "mundo_ordinario":   "Mundo ordinario",
        "llamado":           "El llamado",
        "rechazo":           "Rechazo del llamado",
        "mentor":            "El mentor",
        "cruce_umbral":      "Cruce del umbral",
        "pruebas":           "Pruebas y aliados",
        "caverna":           "La caverna profunda",
        "prueba_suprema":    "La prueba suprema",
        "recompensa":        "La recompensa",
        "camino_regreso":    "Camino de regreso",
        "resurreccion":      "Resurrección",
        "elixir":            "El elixir",
    }

    def __init__(self):
        self.mazo = _construir_mazo_completo()
        self.mayores = [c for c in self.mazo if c["tipo"] == "mayor"]

    def barajar(self, semilla: Optional[int] = None) -> list[dict]:
        mazo_barajado = self.mazo.copy()
        rng = random.Random(semilla)
        rng.shuffle(mazo_barajado)
        return mazo_barajado

    def _barajar_mayores(self, semilla: Optional[int] = None) -> list[dict]:
        mayores = self.mayores.copy()
        rng = random.Random(semilla)
        rng.shuffle(mayores)
        return mayores

    def _hacer_tirada(self, tipo: str, posiciones: list[str], mazo: list[dict], pregunta: str) -> TiradaTarot:
        tirada = TiradaTarot(tipo_tirada=tipo, pregunta=pregunta)
        for i, posicion in enumerate(posiciones):
            ci = mazo[i]
            tirada.cartas.append(CartaTarot(
                id=ci["id"],
                nombre=ci["nombre"],
                tipo=ci["tipo"],
                palo=ci.get("palo"),
                elemento=ci.get("elemento"),
                numero=ci["numero"],
                palabra_clave=ci["palabra_clave"],
                arquetipo=ci["arquetipo"],
                imagen=ci.get("imagen", ""),
                posicion=posicion,
                visual=ci.get("visual", {}),
            ))
        return tirada

    def tirar_un_arcano(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("un_arcano", ["unica"], self.barajar(semilla), pregunta)

    def tirar_fuerza_flaqueza(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("fuerza_flaqueza", self.POSICIONES_FUERZA_FLAQUEZA, self.barajar(semilla), pregunta)

    def tirar_conflicto(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("el_conflicto", self.POSICIONES_CONFLICTO, self.barajar(semilla), pregunta)

    def tirar_tres_cartas(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("tres_cartas", self.POSICIONES_TRES, self.barajar(semilla), pregunta)

    def tirar_duda(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("la_duda", self.POSICIONES_DUDA, self.barajar(semilla), pregunta)

    def tirar_liberacion(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("la_liberacion", self.POSICIONES_LIBERACION, self.barajar(semilla), pregunta)

    def tirar_heroe_5(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("el_heroe_5", self.POSICIONES_HEROE_5, self.barajar(semilla), pregunta)

    def tirar_mundo(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("el_mundo", self.POSICIONES_MUNDO, self.barajar(semilla), pregunta)

    def tirar_cruz_normal(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("cruz_normal", self.POSICIONES_CRUZ_NORMAL, self.barajar(semilla), pregunta)

    def tirar_yo_realizado(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("yo_realizado", self.POSICIONES_YO_REALIZADO, self.barajar(semilla), pregunta)

    def tirar_viaje_heroe(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        """12 etapas del Viaje del Héroe — solo Arcanos Mayores."""
        return self._hacer_tirada("viaje_heroe", self.POSICIONES_HEROE, self._barajar_mayores(semilla), pregunta)

    def obtener_datos_para_interpretacion(self, tirada: TiradaTarot) -> dict:
        cartas_data = []
        for carta in tirada.cartas:
            visual = carta.visual or {}
            cartas_data.append({
                "nombre": carta.nombre,
                "posicion": self.NOMBRES_POSICIONES.get(carta.posicion, carta.posicion),
                "posicion_clave": carta.posicion,
                "arquetipo": carta.arquetipo,
                "palabra_clave": carta.palabra_clave,
                "palo": carta.palo,
                "elemento": carta.elemento,
                "tipo": carta.tipo,
                "numero": carta.numero,
                "imagen": carta.imagen,
                "visual_colores": visual.get("colores", []),
                "visual_mirada": visual.get("figura_mira", ""),
                "visual_gesto": visual.get("gesto", ""),
                "visual_simbolos": visual.get("simbolos", []),
            })
        return {
            "pregunta": tirada.pregunta,
            "tipo_tirada": tirada.tipo_tirada,
            "cartas": cartas_data,
        }
