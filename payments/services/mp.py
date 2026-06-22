import hashlib
import hmac
import logging

import requests
from django.conf import settings

from ..constants import PACKS, PLANS

logger = logging.getLogger(__name__)

_BASE = 'https://api.mercadopago.com'


def _headers():
    return {
        'Authorization': f'Bearer {settings.MERCADOPAGO_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }


def create_preapproval(plan_slug, user, return_url):
    plan = PLANS[plan_slug]
    payload = {
        'reason': plan['title'],
        'auto_recurring': {
            'frequency': 1,
            'frequency_type': 'months',
            'transaction_amount': plan['price_clp'],
            'currency_id': 'CLP',
        },
        'payer_email': user.email,
        'back_url': return_url,
        'status': 'pending',
    }
    resp = requests.post(f'{_BASE}/preapproval', json=payload, headers=_headers(), timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data['id'], data['init_point']


def get_preapproval(preapproval_id):
    resp = requests.get(f'{_BASE}/preapproval/{preapproval_id}', headers=_headers(), timeout=15)
    resp.raise_for_status()
    return resp.json()


def create_preference(pack_slug, user, success_url, failure_url, pending_url):
    pack = PACKS[pack_slug]
    payload = {
        'items': [{
            'title': pack['title'],
            'quantity': 1,
            'unit_price': pack['price_clp'],
            'currency_id': 'CLP',
        }],
        'payer': {'email': user.email},
        'back_urls': {
            'success': success_url,
            'failure': failure_url,
            'pending': pending_url,
        },
        'auto_return': 'approved',
        'metadata': {
            'pack_slug': pack_slug,
            'user_id': str(user.pk),
        },
    }
    resp = requests.post(f'{_BASE}/checkout/preferences', json=payload, headers=_headers(), timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data['id'], data['init_point']


def cancel_preapproval(preapproval_id):
    resp = requests.patch(
        f'{_BASE}/preapproval/{preapproval_id}',
        json={'status': 'cancelled'},
        headers=_headers(), timeout=15,
    )
    resp.raise_for_status()


def get_payment(payment_id):
    resp = requests.get(f'{_BASE}/v1/payments/{payment_id}', headers=_headers(), timeout=15)
    resp.raise_for_status()
    return resp.json()


def verify_webhook(body, x_signature, x_request_id):
    secret = getattr(settings, 'MERCADOPAGO_WEBHOOK_SECRET', '')
    if not secret:
        logger.warning('MERCADOPAGO_WEBHOOK_SECRET no configurado — webhook aceptado sin verificar')
        return True

    parts = {}
    for part in x_signature.split(','):
        if '=' in part:
            k, v = part.split('=', 1)
            parts[k.strip()] = v.strip()

    ts = parts.get('ts', '')
    v1 = parts.get('v1', '')
    if not v1:
        return False

    data_id = body.get('data', {}).get('id', '')
    manifest = f'id:{data_id};request-id:{x_request_id};ts:{ts};'

    computed = hmac.new(
        secret.encode(), manifest.encode(), hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(computed, v1)
