TALLERES = {
    'taller1-terapeutas': {
        'title': 'Seña — Taller Terapeutas 1-ago (reserva de cupo)',
        'price_clp': 5000,
    },
}

PRODUCTS = {
    'endonautica-ebook': {
        'title': 'Ebook Endonautica',
        # Precio CLP siguiendo la misma conversión ~1000:1 ya usada en PLANS (9.99->9990, 39.99->39990).
        'price_clp': 16990,
        'price_usd': '17.00',
    },
    # Consultoría 1:1 de 60 min (precio fijado por Franco el 2026-10-06). Solo MercadoPago/CLP.
    'consultoria-60': {
        'title': 'Consultoría Endonautas (60 min)',
        'price_clp': 29990,
    },
}

CONSULTORIA_SLUG = 'consultoria-60'
CONSULTORIA_MIN = 60
CONSULTORIA_HORIZONTE_DIAS = 14     # cuántos días hacia adelante se ofrecen horarios
CONSULTORIA_ANTICIPACION_H = 24     # no se puede reservar con menos de esto
CONSULTORIA_RETENCION_MIN = 30      # un horario con pago pendiente queda apartado este tiempo

PLANS = {
    'navegante': {
        'title': 'Plan Navegante',
        'price_clp': 9990,
        'price_usd': '9.99',
    },
    'practicante': {
        'title': 'Plan Practicante',
        'price_clp': 39990,
        'price_usd': '39.99',
    },
}
