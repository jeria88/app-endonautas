"""
Card service for the Fractal Oracle — 33-card system (Yuda, 2023).
Selects a card based on a hash derived from the question.
"""

import hashlib
import random
from datetime import date
from ..models import CartaFractal


class CardService:
    def seleccionar_carta(self, pregunta: str) -> dict:
        """
        Selects a card from the 33-card catalog.
        Uses a deterministic hash so the same question always yields the same card.
        Invertida (reversed) probability: ~30%.
        """
        total = CartaFractal.objects.count()
        if total == 0:
            raise ValueError("No fractal cards in the database. Run seed_fractal first.")

        # Incluye la fecha para que la misma pregunta rote de carta cada día
        seed_str = f"{pregunta.lower().strip()}|{date.today().isoformat()}"
        seed = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16)
        rng = random.Random(seed)

        numero = rng.randint(0, total - 1)
        invertida = rng.random() < 0.30

        carta = CartaFractal.objects.filter(numero=numero).first()
        if not carta:
            carta = CartaFractal.objects.order_by("numero")[numero % total]

        return {
            "carta": carta,
            "invertida": invertida,
        }

    def carta_to_dict(self, carta: CartaFractal, invertida: bool) -> dict:
        return {
            "numero": carta.numero,
            "nombre_arcano": carta.nombre_arcano,
            "verbo": carta.verbo,
            "tipo": carta.tipo,
            "descripcion_breve": carta.descripcion_breve,
            "sefirot_nombre": carta.sefirot_nombre,
            "es_especial": carta.es_especial,
            "invertida": invertida,
        }
