"""
Wrapper SerpBear API para posiciones SEO de keywords.
API key obtenida en: https://serpbear.146.181.39.4.sslip.io → Settings → API Key
"""
import os

import requests

_BASE = 'https://serpbear.146.181.39.4.sslip.io'

_EMPTY = {'serpbear_keywords_top3': {}, 'serpbear_posicion_avg': 0, 'serpbear_subiendo': 0}


def fetch_stats():
    api_key = os.getenv('SERPBEAR_API_KEY', '')
    if not api_key:
        return _EMPTY

    try:
        domains = _get_domains(api_key)
        if not domains:
            return _EMPTY

        domain_id = domains[0]['id']
        keywords = _get_keywords(api_key, domain_id)
        if not keywords:
            return _EMPTY

        return _parse(keywords)
    except Exception:
        return _EMPTY


def _get_domains(api_key):
    r = requests.get(
        f'{_BASE}/api/domains',
        headers={'x-api-key': api_key},
        timeout=8,
        verify=False,
    )
    data = r.json()
    # SerpBear devuelve {"domains": [...]} o lista directa según versión
    if isinstance(data, dict):
        return data.get('domains', [])
    return data or []


def _get_keywords(api_key, domain_id):
    r = requests.get(
        f'{_BASE}/api/keywords',
        params={'id': domain_id},
        headers={'x-api-key': api_key},
        timeout=8,
        verify=False,
    )
    data = r.json()
    if isinstance(data, dict):
        return data.get('keywords', [])
    return data or []


def _parse(keywords):
    # keywords con posición válida (>0)
    validas = [k for k in keywords if k.get('position', 0) > 0]
    if not validas:
        return _EMPTY

    # Top 3 mejores posiciones (número más bajo = mejor)
    top3 = sorted(validas, key=lambda k: k['position'])[:3]
    top3_dict = {k.get('keyword', k.get('name', '?')): k['position'] for k in top3}

    posicion_avg = round(sum(k['position'] for k in validas) / len(validas), 1)

    # Subiendo = change negativo (posición bajó = mejoró en rankings)
    subiendo = sum(1 for k in validas if k.get('change', 0) < 0)

    return {
        'serpbear_keywords_top3': top3_dict,
        'serpbear_posicion_avg': posicion_avg,
        'serpbear_subiendo': subiendo,
    }
