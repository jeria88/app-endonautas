"""
Tarot Terapéutico — lógica de mazo, tiradas e imágenes.

Marco filosófico: Alejandro Jodorowsky, "La Vía del Tarot" (con Marianne Costa).
Deck: Tarot de Marsella (orden Marsella, no RWS).
  — Las cartas no predicen: leen el patrón arquetípico activo.
  — Invertida ≠ opuesto: es la misma energía contraída, no integrada.
  — Las 3 cartas se leen como Raíz–Tallo–Flor, no pasado/presente/futuro.
"""

import random
from dataclasses import dataclass, field
from typing import Optional


# ── Imágenes ──────────────────────────────────────────────────────────────────
# Naming: a01-a21 = Arcanos I-XXI, a22 = El Loco (unnumbered in Marseille).
# b=bastos, c=copas, d=oros, e=espadas; numeración 01-14.

_PALO_LETRA = {"bastos": "b", "copas": "c", "oros": "d", "espadas": "e"}


def _imagen_mayor(numero: int) -> str:
    if numero == 0:  # El Loco
        return "img/tarot/a22.jpg"
    return f"img/tarot/a{numero:02d}.jpg"


def _imagen_menor(palo: str, num: int) -> str:
    letra = _PALO_LETRA.get(palo, "b")
    return f"img/tarot/{letra}{num:02d}.jpg"


# ── Arcanos Mayores (orden Marsella) ──────────────────────────────────────────
# VIII = La Justicia, XI = La Fuerza (orden Marsella, no RWS).

ARCANOS_MAYORES = [
    {"id": 0,  "nombre": "El Loco",              "palabra_clave": "libertad absoluta",    "arquetipo": "El inicio sin condición"},
    {"id": 1,  "nombre": "El Mago",              "palabra_clave": "voluntad consciente",  "arquetipo": "La conciencia que actúa"},
    {"id": 2,  "nombre": "La Sacerdotisa",       "palabra_clave": "sabiduría interior",   "arquetipo": "El saber que no habla"},
    {"id": 3,  "nombre": "La Emperatriz",        "palabra_clave": "creación fértil",      "arquetipo": "La madre que genera"},
    {"id": 4,  "nombre": "El Emperador",         "palabra_clave": "estructura y orden",   "arquetipo": "El padre que sostiene"},
    {"id": 5,  "nombre": "El Papa",              "palabra_clave": "transmisión sagrada",  "arquetipo": "El puente entre mundos"},
    {"id": 6,  "nombre": "Los Enamorados",       "palabra_clave": "elección vital",       "arquetipo": "La encrucijada del deseo"},
    {"id": 7,  "nombre": "El Carro",             "palabra_clave": "voluntad victoriosa",  "arquetipo": "El dominio del impulso"},
    {"id": 8,  "nombre": "La Justicia",          "palabra_clave": "verdad precisa",       "arquetipo": "El equilibrio que corta"},
    {"id": 9,  "nombre": "El Ermitaño",          "palabra_clave": "búsqueda interior",    "arquetipo": "La luz que ilumina desde adentro"},
    {"id": 10, "nombre": "La Rueda de Fortuna",  "palabra_clave": "ciclo en movimiento",  "arquetipo": "El ritmo inevitable del cambio"},
    {"id": 11, "nombre": "La Fuerza",            "palabra_clave": "dominio del instinto", "arquetipo": "El amor que doma la bestia"},
    {"id": 12, "nombre": "El Colgado",           "palabra_clave": "entrega y perspectiva","arquetipo": "La inversión que revela"},
    {"id": 13, "nombre": "La Muerte",            "palabra_clave": "transformación radical","arquetipo": "El fin que abre"},
    {"id": 14, "nombre": "La Templanza",         "palabra_clave": "alquimia y flujo",     "arquetipo": "La mezcla que transforma"},
    {"id": 15, "nombre": "El Diablo",            "palabra_clave": "sombra encadenada",    "arquetipo": "El apego que ilusiona"},
    {"id": 16, "nombre": "La Torre",             "palabra_clave": "derrumbe liberador",   "arquetipo": "La verdad que destruye la mentira"},
    {"id": 17, "nombre": "La Estrella",          "palabra_clave": "esperanza desnuda",    "arquetipo": "La fe sin certeza"},
    {"id": 18, "nombre": "La Luna",              "palabra_clave": "inconsciente profundo", "arquetipo": "El umbral de lo que aún no es"},
    {"id": 19, "nombre": "El Sol",               "palabra_clave": "claridad y alegría",   "arquetipo": "La conciencia plena"},
    {"id": 20, "nombre": "El Juicio",            "palabra_clave": "llamado al despertar", "arquetipo": "La resurrección desde adentro"},
    {"id": 21, "nombre": "El Mundo",             "palabra_clave": "integración total",    "arquetipo": "La danza del ser completo"},
]

# ── Arcanos Menores ───────────────────────────────────────────────────────────
# Elementos según Jodorowsky: Bastos=Fuego (libido vital), Copas=Agua (emoción),
# Espadas=Aire (palabra, mente), Oros=Tierra (cuerpo, materia, recurso).

PALOS_MENORES = [
    {"palo": "bastos",   "elemento": "fuego", "esencia": "el impulso creador, la energía vital, la libido que construye"},
    {"palo": "copas",    "elemento": "agua",  "esencia": "el mundo emocional, el amor, lo que fluye y lo que se evita sentir"},
    {"palo": "espadas",  "elemento": "aire",  "esencia": "la mente, la palabra, el corte, el conflicto que revela la verdad"},
    {"palo": "oros",     "elemento": "tierra","esencia": "el cuerpo, los recursos, la materia, lo que se tiene o se carece"},
]

# Jodorowsky: los números tienen una psicología precisa que se cruza con el elemento del palo.
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
    {"num": 12, "nombre": "Caballero", "significado": "el que busca, la energía en movimiento hacia su destino"},
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
        })
    for palo_info in PALOS_MENORES:
        for num_info in NUMEROS_MENORES:
            mazo.append({
                "id": f"ME-{palo_info['palo'][:3].upper()}-{num_info['num']:02d}",
                "nombre": f"{num_info['nombre']} de {palo_info['palo'].capitalize()}",
                "tipo": "menor",
                "palo": palo_info["palo"],
                "elemento": palo_info["elemento"],
                "numero": num_info["num"],
                "palabra_clave": num_info["significado"],
                "arquetipo": palo_info["esencia"],
                "imagen": _imagen_menor(palo_info["palo"], num_info["num"]),
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
    invertida: bool = False
    posicion: str = ""

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
            "invertida": self.invertida,
            "posicion": self.posicion,
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

    Tiradas disponibles:
    — un_arcano:   1 carta · espejo directo
    — tres_cartas: Raíz–Tallo–Flor (tirada Jodorowsky)
    — cruz_normal: Cruz de 5 cartas
    — cruz_celta:  Cruz Celta de 10 cartas
    — viaje_heroe: 12 etapas solo con Arcanos Mayores (narrativa Campbell)
    """

    # Raíz–Tallo–Flor: la tirada simbólica de Jodorowsky.
    # Raíz = causa profunda (inconsciente). Tallo = presente vivido. Flor = potencial si la energía fluye.
    POSICIONES_TRES = ["raiz", "tallo", "flor"]

    # Cruz de 5: el centro, su sombra (no "obstáculo"), la raíz pasada, el camino, el fundamento.
    POSICIONES_CRUZ_NORMAL = ["presente", "sombra", "pasado", "camino", "fundamento"]

    POSICIONES_CRUZ_CELTA = [
        "presente", "sombra", "pasado", "camino",
        "fundamento", "meta",
        "consultante", "influencias", "esperanzas_miedos", "resultado",
    ]

    POSICIONES_HEROE = [
        "mundo_ordinario", "llamado", "rechazo", "mentor",
        "cruce_umbral", "pruebas", "caverna", "prueba_suprema",
        "recompensa", "camino_regreso", "resurreccion", "elixir",
    ]

    NOMBRES_POSICIONES = {
        # Tirada Jodorowsky
        "raiz":              "Raíz — causa profunda",
        "tallo":             "Tallo — presente vivido",
        "flor":              "Flor — potencial real",
        # Una carta
        "unica":             "Carta espejo",
        # Cruz de 5
        "presente":          "Presente",
        "sombra":            "Sombra — lo que la carta central confronta",
        "pasado":            "Pasado reciente",
        "camino":            "Camino abierto",
        "fundamento":        "Fundamento inconsciente",
        # Cruz Celta extras
        "meta":              "Meta consciente",
        "consultante":       "El consultante",
        "influencias":       "Influencias externas",
        "esperanzas_miedos": "Esperanzas y miedos",
        "resultado":         "Resultado posible",
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

    def _hacer_tirada(self, tipo: str, posiciones: list[str], mazo: list[dict], pregunta: str, semilla) -> TiradaTarot:
        tirada = TiradaTarot(tipo_tirada=tipo, pregunta=pregunta)
        rng = random.Random(semilla)
        for i, posicion in enumerate(posiciones):
            ci = mazo[i]
            # Jodorowsky: invertida = energía contraída, ~30% de probabilidad
            invertida = rng.random() < 0.30
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
                invertida=invertida,
                posicion=posicion,
            ))
        return tirada

    def tirar_un_arcano(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("un_arcano", ["unica"], self.barajar(semilla), pregunta, semilla)

    def tirar_tres_cartas(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        """Tirada Raíz–Tallo–Flor (tirada emblema de Jodorowsky)."""
        return self._hacer_tirada("tres_cartas", self.POSICIONES_TRES, self.barajar(semilla), pregunta, semilla)

    def tirar_cruz_normal(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("cruz_normal", self.POSICIONES_CRUZ_NORMAL, self.barajar(semilla), pregunta, semilla)

    def tirar_cruz_celta(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        return self._hacer_tirada("cruz_celta", self.POSICIONES_CRUZ_CELTA, self.barajar(semilla), pregunta, semilla)

    def tirar_viaje_heroe(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        """12 etapas del Viaje del Héroe — solo Arcanos Mayores."""
        return self._hacer_tirada("viaje_heroe", self.POSICIONES_HEROE, self._barajar_mayores(semilla), pregunta, semilla)

    def obtener_datos_para_interpretacion(self, tirada: TiradaTarot) -> dict:
        cartas_data = []
        for carta in tirada.cartas:
            cartas_data.append({
                "nombre": carta.nombre,
                "estado": "contraída" if carta.invertida else "directa",
                "posicion": self.NOMBRES_POSICIONES.get(carta.posicion, carta.posicion),
                "posicion_clave": carta.posicion,
                "arquetipo": carta.arquetipo,
                "palabra_clave": carta.palabra_clave,
                "palo": carta.palo,
                "elemento": carta.elemento,
                "tipo": carta.tipo,
                "numero": carta.numero,
                "imagen": carta.imagen,
            })
        return {
            "pregunta": tirada.pregunta,
            "tipo_tirada": tirada.tipo_tirada,
            "cartas": cartas_data,
        }
