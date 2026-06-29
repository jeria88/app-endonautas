"""
Wrapper Umami API para tráfico de landing.
Docs: https://umami.is/docs/api
"""
import os
from datetime import timedelta

import requests

_BASE = 'https://analytics.146.181.39.4.sslip.io'
_WEBSITE_ID = os.getenv('UMAMI_WEBSITE_ID', 'e03fa69e-9931-411c-9838-7f6ffea90426')


def _token():
    api_key = os.getenv('UMAMI_API_KEY', '')
    if api_key:
        return {'x-umami-api-key': api_key}
    # fallback: autenticación básica si hay user/pass configurados
    user = os.getenv('UMAMI_USER', '')
    pwd = os.getenv('UMAMI_PASSWORD', '')
    if user and pwd:
        r = requests.post(
            f'{_BASE}/api/auth/login',
            json={'username': user, 'password': pwd},
            timeout=8,
        )
        token = r.json().get('token', '')
        return {'Authorization': f'Bearer {token}'}
    return {}


def fetch_week_stats(week_start):
    """
    Devuelve pageviews, visitantes únicos y top fuentes (referrers).
    """
    week_end = week_start + timedelta(days=7)
    start_at = int(week_start.strftime('%s')) * 1000
    end_at = int(week_end.strftime('%s')) * 1000

    try:
        headers = _token()
        stats = _get_stats(start_at, end_at, headers)
        fuentes = _get_referrers(start_at, end_at, headers)
        return {
            'visitas_landing': stats.get('pageviews', {}).get('value', 0),
            'visitas_unicas': stats.get('visitors', {}).get('value', 0),
            'fuentes_top': fuentes,
        }
    except Exception:
        return {'visitas_landing': 0, 'visitas_unicas': 0, 'fuentes_top': {}}


def _get_stats(start_at, end_at, headers):
    r = requests.get(
        f'{_BASE}/api/websites/{_WEBSITE_ID}/stats',
        params={'startAt': start_at, 'endAt': end_at},
        headers=headers,
        timeout=8,
    )
    return r.json()


def _get_referrers(start_at, end_at, headers):
    r = requests.get(
        f'{_BASE}/api/websites/{_WEBSITE_ID}/referrers',
        params={'startAt': start_at, 'endAt': end_at, 'limit': 5},
        headers=headers,
        timeout=8,
    )
    data = r.json()
    if isinstance(data, list):
        total = sum(item.get('y', 0) for item in data) or 1
        return {item['x']: round(item['y'] / total * 100, 1) for item in data[:5]}
    return {}
