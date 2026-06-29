"""
Wrapper Listmonk API para métricas de email marketing.
Reutiliza credenciales de accounts/listmonk.py.
"""
import base64
from datetime import timedelta

import requests

_BASE = 'https://mail.146.181.39.4.sslip.io'
_USER = 'api_claude'
_TOKEN = 'lm_api_2b99334cb53a67a428a364049b45b986533908952a897102'


def _headers():
    creds = base64.b64encode(f'{_USER}:{_TOKEN}'.encode()).decode()
    return {'Authorization': f'Basic {creds}', 'Content-Type': 'application/json'}


def fetch_week_stats(week_start):
    """
    Devuelve dict con open_rate, CTR y total suscriptores.
    Las campañas enviadas en la semana dada se promedian.
    Si falla, devuelve valores en 0.
    """
    week_end = week_start + timedelta(days=7)
    try:
        camps = _get_campaigns_in_week(week_start, week_end)
        open_rates, ctrs = [], []
        for c in camps:
            stats = _get_campaign_stats(c['id'])
            total = stats.get('sent', 0)
            if total > 0:
                open_rates.append(stats.get('views', 0) / total * 100)
                ctrs.append(stats.get('clicks', 0) / total * 100)

        subs = _get_total_subscribers()

        return {
            'email_open_rate_pct': round(sum(open_rates) / len(open_rates), 1) if open_rates else 0.0,
            'email_ctr_pct': round(sum(ctrs) / len(ctrs), 1) if ctrs else 0.0,
            'suscriptores_total': subs,
        }
    except Exception:
        return {'email_open_rate_pct': 0.0, 'email_ctr_pct': 0.0, 'suscriptores_total': 0}


def _get_campaigns_in_week(week_start, week_end):
    r = requests.get(
        f'{_BASE}/api/campaigns',
        params={'page': 1, 'per_page': 50, 'status': 'finished'},
        headers=_headers(),
        timeout=8,
    )
    all_camps = r.json().get('data', {}).get('results', [])
    return [
        c for c in all_camps
        if c.get('send_at') and week_start.isoformat() <= c['send_at'][:10] < week_end.isoformat()
    ]


def _get_campaign_stats(campaign_id):
    r = requests.get(
        f'{_BASE}/api/campaigns/{campaign_id}/stats',
        headers=_headers(),
        timeout=8,
    )
    return r.json().get('data', {})


def _get_total_subscribers():
    r = requests.get(
        f'{_BASE}/api/subscribers',
        params={'per_page': 1},
        headers=_headers(),
        timeout=8,
    )
    return r.json().get('data', {}).get('total', 0)
