"""Los 6 emails de la campaña del ebook que corren diferidos (T1 y P1 salen inline
desde las views y no están acá).

Ramas:
  A · nutrición del test  — T2 (+2d), T3 (+4d)   — personalizados por herida
  B · carrito abandonado  — A1 (+1h), A2 (+24h)
  C · post-compra         — P2 (+3d), P3 (+7d)

Cada función:
  - nunca lanza (patrón de `entrega.py`),
  - respeta `EbookOptOut` y excluye `FRANCO_EMAIL`,
  - es idempotente: reclama la fila `EbookFunnelEmail(email, step)` antes de mandar
    y la borra si el envío falla (así la próxima corrida reintenta).

El comando `run_ebook_funnel` decide a quién le toca cada paso y en qué orden de
precedencia. Estas funciones solo arman y mandan.
"""
import json
import logging
import os

from django.conf import settings
from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

from .constants import PRODUCTS
from .models import EbookFunnelEmail, EbookLead, EbookOptOut

logger = logging.getLogger(__name__)

BAJA_SALT = 'ebook-baja-v1'
_HERIDAS_PATH = os.path.join(os.path.dirname(__file__), 'ebook_files', 'heridas.json')
_FIRMA = '— Franco'


def _heridas():
    try:
        with open(_HERIDAS_PATH, encoding='utf-8') as f:
            return {h['id']: h for h in json.load(f)}
    except Exception:
        return {}


def _precio():
    p = PRODUCTS['endonautica-ebook']
    return f"{p['price_usd'].split('.')[0]} dólares ({int(p['price_clp']):,} pesos)".replace(',', '.')


def _sitio():
    return settings.PUBLIC_SITE_URL.rstrip('/')


def _link_checkout(herida=''):
    return f'{_sitio()}/?herida={herida}' if herida else _sitio()


def _link_circulo():
    return f'{_sitio()}/circulo/'


def _baja_url(email):
    token = signing.dumps(email, salt=BAJA_SALT)
    return f"{settings.APP_BASE_URL.rstrip('/')}{reverse('pago_ebook_baja', args=[token])}"


def _saludo(nombre):
    nombre = (nombre or '').strip()
    return f'{nombre}, ' if nombre else ''


def _herida_de(email):
    """La herida más reciente registrada para ese email en un EbookLead."""
    lead = (EbookLead.objects.filter(email__iexact=email).exclude(herida='')
            .order_by('-created_at').first())
    return lead.herida if lead else ''


def _send(step, email, subject, body_text):
    email = (email or '').strip().lower()
    if not email:
        return False
    if email == (settings.FRANCO_EMAIL or '').strip().lower():
        return False
    if EbookOptOut.objects.filter(email=email).exists():
        return False

    obj, created = EbookFunnelEmail.objects.get_or_create(email=email, step=step)
    if not created:
        return False  # ya se mandó (o lo está mandando otra corrida)

    try:
        baja = _baja_url(email)
        cuerpo = f'{body_text}\n\n—\nSi no quieres más correos sobre el libro: {baja}'
        msg = EmailMultiAlternatives(subject, cuerpo, to=[email])
        msg.extra_headers['List-Unsubscribe'] = (
            f'<mailto:{settings.DEFAULT_FROM_EMAIL}?subject=baja>, <{baja}>'
        )
        msg.extra_headers['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click'
        msg.send(fail_silently=False)
    except Exception as e:
        logger.error(f'funnel_emails {step} {email}: {e}')
        obj.delete()
        return False
    return True


# --- Rama B · carrito abandonado -------------------------------------------------

def enviar_A1(order):
    nombre = (order.user.first_name or '').strip()
    herida = _herida_de(order.user.email)
    cuerpo = (
        f'{_saludo(nombre)}escribiste tu correo para llevarte La Endonáutica y algo '
        'cortó el paso justo antes de pagar. Pasa: se cae la conexión, entra una '
        'llamada, la vida real interrumpe.\n\n'
        'El libro sigue disponible y la descarga es inmediata — PDF ilustrado y EPUB, '
        'apenas se confirma el pago.\n\n'
        'Si algo no funcionó o tienes una duda antes de comprar, respóndeme este '
        'correo. Lo leo yo.\n\n'
        f'→ {_link_checkout(herida)}\n\n'
        f'{_FIRMA}'
    )
    return _send('A1', order.user.email, 'Dejaste el mapa a medio abrir', cuerpo)


def enviar_A2(order):
    nombre = (order.user.first_name or '').strip()
    herida = _herida_de(order.user.email)
    cuerpo = (
        f'{_saludo(nombre)}ayer estuviste a un clic de llevarte el libro.\n\n'
        'Te escribo porque conozco esa pausa. No es sobre el precio — es que ponerle '
        'nombre a lo que uno repite exige una cosa que la mayoría posterga: dejar de '
        'mirar para afuera.\n\n'
        'La Endonáutica no es un libro para sentirte mejor un rato. Es un sistema para '
        'observar tu mundo interior con precisión: la herida de infancia, la máscara '
        'que armaste sobre ella, la sombra leída como información y no como enemigo. '
        '205 páginas, mi marco completo.\n\n'
        'Si el momento no es ahora, está bien. Si lo es, aquí sigue:\n\n'
        f'→ {_link_checkout(herida)}\n\n'
        f'{_FIRMA}'
    )
    return _send('A2', order.user.email, 'Lo que cuesta empezar a mirarse', cuerpo)


# --- Rama C · post-compra ------------------------------------------------------

def enviar_P2(order):
    nombre = (order.user.first_name or '').strip()
    cuerpo = (
        f'{_saludo(nombre)}ya llevas unos días con el libro.\n\n'
        'Si llegaste a los capítulos de la herida y la máscara, quizás notaste algo: '
        'hay conceptos que reconoces de inmediato, y otros que te dan ganas de saltar. '
        'Esos segundos son los que importan. La resistencia marca dónde está el '
        'trabajo.\n\n'
        'No hace falta leerlo entero de una vez. Vuelve a los esquemas — los pilares '
        'del endonauta, el mapa de niveles de conciencia — y úsalos como espejo de '
        'dónde estás hoy.\n\n'
        '¿Cuál de los pilares te resonó más hasta ahora? Respóndeme, los leo todos.\n\n'
        f'{_FIRMA}'
    )
    return _send('P2', order.user.email, '¿Qué te generó resistencia?', cuerpo)


def enviar_P3(order):
    nombre = (order.user.first_name or '').strip()
    cuerpo = (
        f'{_saludo(nombre)}a esta altura ya tienes el marco: la teoría, la estructura, '
        'el vocabulario para nombrar lo que antes solo se repetía.\n\n'
        'Pero como sabe cualquiera que caminó un proceso: el mapa no es el territorio. '
        'La teoría del autoconocimiento necesita práctica sostenida para no evaporarse '
        'cuando la rutina vuelve.\n\n'
        'La Endonáutica es la primera pieza de algo más grande. La siguiente es el '
        'Círculo Endonauta: un grupo pequeño que trabaja este material en profundidad, '
        'acompañado, durante varias semanas. Se abre por cupo unas pocas veces al '
        'año.\n\n'
        'Si quieres saber cuándo abre la próxima, deja tu nombre en la lista de espera '
        '— no compromete a nada:\n\n'
        f'→ {_link_circulo()}\n\n'
        'Y si el libro te sirvió, me ayudas mucho respondiéndome con tu experiencia, o '
        'pasándoselo a alguien que necesite este mapa.\n\n'
        f'{_FIRMA}'
    )
    return _send('P3', order.user.email, 'El mapa no es el territorio', cuerpo)


# --- Rama A · nutrición del test (personalizados por herida) ------------------

def enviar_T2(lead):
    h = _heridas().get(lead.herida, {})
    herida = h.get('herida', 'infancia').lower()
    corta = h.get('mascaraCorta', '')
    frase = h.get('frase', '')
    de_mascara = f' — la de {corta}' if corta else ''
    bloque_frase = f'{frase}\n\n' if frase else ''
    cuerpo = (
        f'Hace un par de días viste tu herida de {herida} y la máscara que armaste '
        f'encima{de_mascara}.\n\n'
        'Esa máscara funciona. Por eso la sostienes. Pero funciona a un costo, y el '
        'costo es energía.\n\n'
        f'{bloque_frase}'
        'La medicina china lo describe como un ciclo de control: un elemento que se '
        'desregula obliga al resto del sistema a compensar, todo el día, sin que lo '
        'notes. Vivir en guardia cansa de un modo que el descanso no arregla.\n\n'
        'En La Endonáutica desarmo ese ciclo pieza por pieza: los cinco elementos, '
        'cómo se controlan entre sí, y qué hacer cuando uno se lleva toda la energía. '
        'No es filosofía — es un motor que ya está operando dentro de ti.\n\n'
        f'El libro, con la página adaptada a tu herida:\n→ {_link_checkout(lead.herida)}\n\n'
        f'{_FIRMA}'
    )
    return _send('T2', lead.email, 'La cuenta que paga tu máscara', cuerpo)


def enviar_T3(lead):
    h = _heridas().get(lead.herida, {})
    herida = h.get('herida', 'infancia').lower()
    cuerpo = (
        f'Hiciste el test, leíste el mapa de tu herida de {herida}. Ya sabes qué '
        'operas y cómo se llama.\n\n'
        'Saberlo no lo cambia. Lo que cambia las cosas es tener el marco completo para '
        'trabajarlo — y salir de la inercia, que suele ser la parte más difícil.\n\n'
        f'La Endonáutica cuesta {_precio()}. 205 páginas: las cinco heridas, las '
        'máscaras, la sombra, los cinco elementos, el mapa de niveles de conciencia. '
        'El bisturí, no el diagnóstico.\n\n'
        f'Con la página adaptada a tu perfil:\n→ {_link_checkout(lead.herida)}\n\n'
        'Si tienes una duda antes de comprar, respóndeme. Lo leo yo.\n\n'
        f'{_FIRMA}'
    )
    return _send('T3', lead.email, 'Ya sabes qué tienes', cuerpo)
