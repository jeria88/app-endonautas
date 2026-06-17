"""
Servicios del Tarot Terapéutico (Enfoque Junguiano y Narrativo).

Lógica pura: barajado, selección de tiradas, generación de interpretaciones.
No depende de Django — se puede testear independientemente.
"""

import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════
# DATOS DEL MAZO: 78 cartas (22 Mayores + 56 Menores)
# ═══════════════════════════════════════════════════

ARCANOS_MAYORES = [
    {"id": 0, "nombre": "El Loco", "palabra_clave": "inocencia", "arquetipo": "El viaje comienza"},
    {"id": 1, "nombre": "El Mago", "palabra_clave": "poder", "arquetipo": "Consciencia y voluntad"},
    {"id": 2, "nombre": "La Sacerdotisa", "palabra_clave": "intuición", "arquetipo": "Sabiduría oculta"},
    {"id": 3, "nombre": "La Emperatriz", "palabra_clave": "abundancia", "arquetipo": "Fertilidad y creación"},
    {"id": 4, "nombre": "El Emperador", "palabra_clave": "estructura", "arquetipo": "Autoridad y orden"},
    {"id": 5, "nombre": "El Hierofante", "palabra_clave": "tradición", "arquetipo": "Enseñanza espiritual"},
    {"id": 6, "nombre": "Los Enamorados", "palabra_clave": "elección", "arquetipo": "Unión y decisión"},
    {"id": 7, "nombre": "El Carro", "palabra_clave": "voluntad", "arquetipo": "Victoria y determinación"},
    {"id": 8, "nombre": "La Fuerza", "palabra_clave": "coraje", "arquetipo": "Fuerza interior"},
    {"id": 9, "nombre": "El Ermitaño", "palabra_clave": "búsqueda", "arquetipo": "Introspección y soledad"},
    {"id": 10, "nombre": "La Rueda de la Fortuna", "palabra_clave": "ciclo", "arquetipo": "Destino y cambio"},
    {"id": 11, "nombre": "La Justicia", "palabra_clave": "equilibrio", "arquetipo": "Verdad y consecuencia"},
    {"id": 12, "nombre": "El Colgado", "palabra_clave": "perspectiva", "arquetipo": "Sacrificio y nueva visión"},
    {"id": 13, "nombre": "La Muerte", "palabra_clave": "transformación", "arquetipo": "Fin y renacimiento"},
    {"id": 14, "nombre": "La Templanza", "palabra_clave": "integración", "arquetipo": "Alquimia y paciencia"},
    {"id": 15, "nombre": "El Diablo", "palabra_clave": "sombra", "arquetipo": "Apego y materialismo"},
    {"id": 16, "nombre": "La Torre", "palabra_clave": "revelación", "arquetipo": "Derrumbe y verdad"},
    {"id": 17, "nombre": "La Estrella", "palabra_clave": "esperanza", "arquetipo": "Inspiración y sanación"},
    {"id": 18, "nombre": "La Luna", "palabra_clave": "ilusión", "arquetipo": "Inconsciente y miedo"},
    {"id": 19, "nombre": "El Sol", "palabra_clave": "claridad", "arquetipo": "Alegría y vitalidad"},
    {"id": 20, "nombre": "El Juicio", "palabra_clave": "renacimiento", "arquetipo": "Evaluación y despertar"},
    {"id": 21, "nombre": "El Mundo", "palabra_clave": "completitud", "arquetipo": "Integración y logro"},
]

PALOS_MENORES = [
    {"palo": "bastos", "elemento": "fuego", "tematica": "acción, creatividad, impulso"},
    {"palo": "copas", "elemento": "agua", "tematica": "emociones, relaciones, intuición"},
    {"palo": "espadas", "elemento": "aire", "tematica": "pensamiento, conflicto, verdad"},
    {"palo": "oros", "elemento": "tierra", "tematica": "material, cuerpo, recursos"},
]

NUMEROS_MENORES = [
    {"num": 1, "nombre": "As", "significado": "semilla, inicio, potencial"},
    {"num": 2, "nombre": "Dos", "significado": "dualidad, elección, partnership"},
    {"num": 3, "nombre": "Tres", "significado": "creación, expansión, síntesis"},
    {"num": 4, "nombre": "Cuatro", "significado": "estabilidad, estructura, fundamento"},
    {"num": 5, "nombre": "Cinco", "significado": "conflicto, cambio, desafío"},
    {"num": 6, "nombre": "Seis", "significado": "armonía, resolución, equilibrio"},
    {"num": 7, "nombre": "Siete", "significado": "reflexión, evaluación, sabiduría"},
    {"num": 8, "nombre": "Ocho", "significado": "movimiento, poder, maestría"},
    {"num": 9, "nombre": "Nueve", "significado": "satisfacción, logro, soledad"},
    {"num": 10, "nombre": "Diez", "significado": "culminación, cierre, transición"},
    {"num": 11, "nombre": "Sota", "significado": "exploración, mensaje, juventud"},
    {"num": 12, "nombre": "Caballero", "significado": "acción, búsqueda, impulso"},
    {"num": 13, "nombre": "Reina", "significado": "nutrición, madurez, poder interior"},
    {"num": 14, "nombre": "Rey", "significado": "maestría, autoridad, realización"},
]


def _construir_mazo_completo() -> list[dict]:
    """Construye el mazo completo de 78 cartas."""
    mazo = []

    # 22 Arcanos Mayores
    for arcano in ARCANOS_MAYORES:
        mazo.append({
            "id": f"AM-{arcano['id']:02d}",
            "nombre": arcano["nombre"],
            "tipo": "mayor",
            "palo": None,
            "numero": arcano["id"],
            "palabra_clave": arcano["palabra_clave"],
            "arquetipo": arcano["arquetipo"],
        })

    # 56 Arcanos Menores (14 por palo × 4 palos)
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
                "arquetipo": palo_info["tematica"],
            })

    return mazo


@dataclass
class CartaTarot:
    """Representación de una carta en la tirada."""
    id: str
    nombre: str
    tipo: str  # "mayor" o "menor"
    palo: Optional[str]
    numero: int
    palabra_clave: str
    arquetipo: str
    invertida: bool = False
    posicion: str = ""  # Posición en la tirada

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "palo": self.palo,
            "numero": self.numero,
            "palabra_clave": self.palabra_clave,
            "arquetipo": self.arquetipo,
            "invertida": self.invertida,
            "posicion": self.posicion,
        }


@dataclass
class TiradaTarot:
    """Resultado completo de una tirada de tarot."""
    tipo_tirada: str
    cartas: list[CartaTarot] = field(default_factory=list)
    pregunta: str = ""

    def to_dict(self) -> dict:
        return {
            "tipo_tirada": self.tipo_tirada,
            "pregunta": self.pregunta,
            "cartas": [c.to_dict() for c in self.cartas],
        }


class TarotService:
    """
    Servicio principal del Tarot Terapéutico.
    Maneja barajado, selección de tiradas y preparación de datos
    para interpretación.
    """

    POSICIONES_TRES = ["origen", "situacion", "potencial"]

    # Cruz Normal (5 cartas): centro + los 4 puntos cardinales
    POSICIONES_CRUZ_NORMAL = ["presente", "obstaculo", "pasado", "futuro_cercano", "fundamento"]

    # Cruz Celta completa (10 cartas)
    POSICIONES_CRUZ_CELTA = [
        "presente", "obstaculo", "pasado", "futuro_cercano",
        "fundamento", "meta",
        "consultante", "influencias", "esperanzas_miedos", "resultado",
    ]

    # Viaje del Héroe (12 etapas, solo Arcanos Mayores)
    POSICIONES_HEROE = [
        "mundo_ordinario", "llamado", "rechazo", "mentor",
        "cruce_umbral", "pruebas", "caverna", "prueba_suprema",
        "recompensa", "camino_regreso", "resurreccion", "elixir",
    ]

    NOMBRES_POSICIONES = {
        "origen": "Origen (Pasado temático)",
        "situacion": "Situación (Presente)",
        "potencial": "Potencial (Futuro como posibilidad)",
        "presente": "Presente",
        "obstaculo": "Obstáculo / Cruz",
        "pasado": "Pasado",
        "futuro_cercano": "Futuro Cercano",
        "fundamento": "Fundamento (Base inconsciente)",
        "meta": "Meta / Conciencia Superior",
        "consultante": "El Consultante",
        "influencias": "Influencias Externas",
        "esperanzas_miedos": "Esperanzas y Miedos",
        "resultado": "Resultado Potencial",
        "unica": "Carta Única",
        # Viaje del Héroe
        "mundo_ordinario": "Mundo Ordinario",
        "llamado": "El Llamado a la Aventura",
        "rechazo": "Rechazo del Llamado",
        "mentor": "El Mentor",
        "cruce_umbral": "Cruce del Primer Umbral",
        "pruebas": "Pruebas, Aliados y Enemigos",
        "caverna": "La Caverna Más Profunda",
        "prueba_suprema": "La Prueba Suprema",
        "recompensa": "La Recompensa",
        "camino_regreso": "El Camino de Regreso",
        "resurreccion": "La Resurrección",
        "elixir": "El Regreso con el Elixir",
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
            carta_info = mazo[i]
            invertida = rng.random() > 0.5
            tirada.cartas.append(CartaTarot(
                id=carta_info["id"],
                nombre=carta_info["nombre"],
                tipo=carta_info["tipo"],
                palo=carta_info.get("palo"),
                numero=carta_info["numero"],
                palabra_clave=carta_info["palabra_clave"],
                arquetipo=carta_info["arquetipo"],
                invertida=invertida,
                posicion=posicion,
            ))
        return tirada

    def tirar_un_arcano(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        """Una sola carta — lectura directa."""
        mazo = self.barajar(semilla)
        return self._hacer_tirada("un_arcano", ["unica"], mazo, pregunta, semilla)

    def tirar_tres_cartas(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        """Tirada de 3 cartas: Origen–Situación–Potencial."""
        mazo = self.barajar(semilla)
        return self._hacer_tirada("tres_cartas", self.POSICIONES_TRES, mazo, pregunta, semilla)

    def tirar_cruz_normal(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        """Cruz simple de 5 cartas."""
        mazo = self.barajar(semilla)
        return self._hacer_tirada("cruz_normal", self.POSICIONES_CRUZ_NORMAL, mazo, pregunta, semilla)

    def tirar_cruz_celta(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        """Cruz Celta completa: 10 cartas."""
        mazo = self.barajar(semilla)
        return self._hacer_tirada("cruz_celta", self.POSICIONES_CRUZ_CELTA, mazo, pregunta, semilla)

    def tirar_viaje_heroe(self, pregunta: str, semilla: Optional[int] = None) -> TiradaTarot:
        """Viaje del Héroe: 12 etapas usando solo los 22 Arcanos Mayores."""
        mayores = self._barajar_mayores(semilla)
        return self._hacer_tirada("viaje_heroe", self.POSICIONES_HEROE, mayores, pregunta, semilla)

    def obtener_datos_para_interpretacion(self, tirada: TiradaTarot) -> dict:
        cartas_data = []
        for carta in tirada.cartas:
            estado = "invertida" if carta.invertida else "derecha"
            cartas_data.append({
                "nombre": carta.nombre,
                "estado": estado,
                "posicion": self.NOMBRES_POSICIONES.get(carta.posicion, carta.posicion),
                "arquetipo": carta.arquetipo,
                "palabra_clave": carta.palabra_clave,
                "palo": carta.palo,
                "tipo": carta.tipo,
            })

        return {
            "pregunta": tirada.pregunta,
            "tipo_tirada": tirada.tipo_tirada,
            "cartas": cartas_data,
        }
