"""Meta Conversions API — envío server-side del evento Purchase del ebook.
Redundante a propósito con el pixel client-side (_resultado_body.html): mismo
event_id en los dos para que Meta los deduplique. Nunca debe romper el flujo
de pago — cualquier error acá se loguea y se traga."""
import hashlib
import logging
import time

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_GRAPH = 'https://graph.facebook.com/v21.0'


def _hash(value):
    return hashlib.sha256(value.strip().lower().encode('utf-8')).hexdigest()


def send_purchase(order, request=None):
    """order: EbookOrder ya marcado como pagado. request: opcional (None en
    el camino del webhook, que no tiene request de navegador)."""
    if not settings.META_CAPI_ACCESS_TOKEN or not settings.META_PIXEL_ID:
        return

    event = {
        'event_name': 'Purchase',
        'event_time': int(time.time()),
        'event_id': f'purchase-{order.pk}',
        'action_source': 'website',
        'user_data': {'em': [_hash(order.user.email)]},
        'custom_data': {
            'value': float(order.amount_local),
            'currency': order.currency,
        },
    }
    if request is not None:
        event['event_source_url'] = request.build_absolute_uri()
        event['user_data']['client_ip_address'] = request.META.get('REMOTE_ADDR', '')
        event['user_data']['client_user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        fbp = request.COOKIES.get('_fbp')
        fbc = request.COOKIES.get('_fbc')
        if fbp:
            event['user_data']['fbp'] = fbp
        if fbc:
            event['user_data']['fbc'] = fbc

    try:
        resp = requests.post(
            f'{_GRAPH}/{settings.META_PIXEL_ID}/events',
            params={'access_token': settings.META_CAPI_ACCESS_TOKEN},
            json={'data': [event]},
            timeout=10,
        )
        if resp.status_code >= 400:
            logger.error(f'Meta CAPI Purchase error order={order.pk}: {resp.text}')
    except Exception as e:
        logger.error(f'Meta CAPI Purchase exception order={order.pk}: {e}')
