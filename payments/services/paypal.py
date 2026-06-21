import logging

import requests
from django.conf import settings

from ..constants import PACKS, PLANS

logger = logging.getLogger(__name__)

_BASE_LIVE = 'https://api.paypal.com'
_BASE_SANDBOX = 'https://api.sandbox.paypal.com'


def _base():
    return _BASE_LIVE if getattr(settings, 'PAYPAL_MODE', 'sandbox') == 'live' else _BASE_SANDBOX


def _get_access_token():
    resp = requests.post(
        f'{_base()}/v1/oauth2/token',
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
        data={'grant_type': 'client_credentials'},
        headers={'Accept': 'application/json'},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()['access_token']


def _headers():
    return {
        'Authorization': f'Bearer {_get_access_token()}',
        'Content-Type': 'application/json',
    }


PLAN_IDS = {
    'navegante': 'P-4K440715A0373301RNI4GLKI',
    'practicante': 'P-2R147097HR919335HNI4GLKI',
}


def create_subscription(plan_slug, return_url, cancel_url, user_email):
    plan_id = PLAN_IDS[plan_slug]
    payload = {
        'plan_id': plan_id,
        'subscriber': {'email_address': user_email},
        'application_context': {
            'return_url': return_url,
            'cancel_url': cancel_url,
            'shipping_preference': 'NO_SHIPPING',
            'user_action': 'SUBSCRIBE_NOW',
            'brand_name': 'Endonautas',
        },
    }
    resp = requests.post(
        f'{_base()}/v1/billing/subscriptions',
        json=payload, headers=_headers(), timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    approve_url = next(lnk['href'] for lnk in data['links'] if lnk['rel'] == 'approve')
    return data['id'], approve_url


def get_subscription(subscription_id):
    resp = requests.get(
        f'{_base()}/v1/billing/subscriptions/{subscription_id}',
        headers=_headers(), timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def create_order(pack_slug, return_url, cancel_url):
    pack = PACKS[pack_slug]
    payload = {
        'intent': 'CAPTURE',
        'purchase_units': [{
            'amount': {'currency_code': 'USD', 'value': pack['price_usd']},
            'description': pack['title'],
        }],
        'application_context': {
            'return_url': return_url,
            'cancel_url': cancel_url,
            'brand_name': 'Endonautas',
            'shipping_preference': 'NO_SHIPPING',
            'user_action': 'PAY_NOW',
        },
    }
    resp = requests.post(
        f'{_base()}/v2/checkout/orders',
        json=payload, headers=_headers(), timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    approve_url = next(lnk['href'] for lnk in data['links'] if lnk['rel'] == 'approve')
    return data['id'], approve_url


def capture_order(order_id):
    resp = requests.post(
        f'{_base()}/v2/checkout/orders/{order_id}/capture',
        json={}, headers=_headers(), timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def verify_webhook_signature(request_headers, raw_body):
    webhook_id = getattr(settings, 'PAYPAL_WEBHOOK_ID', '')
    if not webhook_id:
        logger.warning('PAYPAL_WEBHOOK_ID no configurado — webhook no verificado')
        return False

    payload = {
        'auth_algo': request_headers.get('PAYPAL-AUTH-ALGO', ''),
        'cert_url': request_headers.get('PAYPAL-CERT-URL', ''),
        'transmission_id': request_headers.get('PAYPAL-TRANSMISSION-ID', ''),
        'transmission_sig': request_headers.get('PAYPAL-TRANSMISSION-SIG', ''),
        'transmission_time': request_headers.get('PAYPAL-TRANSMISSION-TIME', ''),
        'webhook_id': webhook_id,
        'webhook_event': raw_body,
    }
    try:
        resp = requests.post(
            f'{_base()}/v1/notifications/verify-webhook-signature',
            json=payload, headers=_headers(), timeout=15,
        )
        return resp.status_code == 200 and resp.json().get('verification_status') == 'SUCCESS'
    except Exception as e:
        logger.error(f'PayPal webhook verification error: {e}')
        return False
