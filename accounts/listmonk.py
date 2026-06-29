"""
Cliente Listmonk para integración programática desde la app.
Todas las funciones fallan silenciosamente — nunca bloquean el flujo principal.
"""
import base64

import requests

_BASE = 'https://mail.endonautas.cl'
_USER = 'api_claude'
_TOKEN = 'lm_api_2b99334cb53a67a428a364049b45b986533908952a897102'

LIST_USUARIOS_APP = 4
LIST_LEADS_APP = 7
LIST_PRACTICANTES = 5

_PLAN_LISTS = {
    'free':        [LIST_USUARIOS_APP, LIST_LEADS_APP],
    'navegante':   [LIST_USUARIOS_APP],
    'practicante': [LIST_USUARIOS_APP, LIST_PRACTICANTES],
    'empresa':     [LIST_USUARIOS_APP, LIST_PRACTICANTES],
}

WELCOME_TEMPLATE_ID = 7
KPI_REPORT_TEMPLATE_ID = int(__import__('os').getenv('LISTMONK_TX_KPI_TEMPLATE_ID', '0'))


def _headers():
    creds = base64.b64encode(f'{_USER}:{_TOKEN}'.encode()).decode()
    return {'Authorization': f'Basic {creds}', 'Content-Type': 'application/json'}


def subscribe_user(email, plan='free', name=''):
    """Suscribe al email en las listas correspondientes al plan dado."""
    list_ids = _PLAN_LISTS.get(plan, [LIST_USUARIOS_APP])
    try:
        requests.post(
            f'{_BASE}/api/subscribers',
            json={
                'email': email,
                'name': name or email.split('@')[0],
                'status': 'enabled',
                'lists': list_ids,
                'preconfirm_subscriptions': True,
            },
            headers=_headers(),
            timeout=5,
        )
    except Exception:
        pass


def update_subscriber_lists(email, plan):
    """Actualiza las listas cuando el usuario cambia de plan."""
    list_ids = _PLAN_LISTS.get(plan, [LIST_USUARIOS_APP])
    try:
        r = requests.get(
            f'{_BASE}/api/subscribers',
            params={'query': f'subscribers.email = \'{email}\'', 'per_page': 1},
            headers=_headers(),
            timeout=5,
        )
        data = r.json()
        subscribers = data.get('data', {}).get('results', [])
        if not subscribers:
            return
        sub_id = subscribers[0]['id']
        requests.post(
            f'{_BASE}/api/subscribers/lists',
            json={
                'ids': [sub_id],
                'action': 'add',
                'target_list_ids': list_ids,
                'status': 'confirmed',
            },
            headers=_headers(),
            timeout=5,
        )
    except Exception:
        pass


def send_weekly_kpi_email(html_body, escenario, week_number, franco_email=None):
    """Envía reporte KPI semanal vía Listmonk TX."""
    if not KPI_REPORT_TEMPLATE_ID:
        return
    email = franco_email or __import__('os').getenv('FRANCO_EMAIL', 'fjeriacastro@gmail.com')
    try:
        requests.post(
            f'{_BASE}/api/tx',
            json={
                'subscriber_email': email,
                'template_id': KPI_REPORT_TEMPLATE_ID,
                'data': {'week_number': week_number, 'escenario': escenario, 'html_body': html_body},
            },
            headers=_headers(),
            timeout=8,
        )
    except Exception:
        pass


def send_welcome_email(email, name=''):
    """Envía email de bienvenida vía Listmonk TX (template ID 7)."""
    try:
        requests.post(
            f'{_BASE}/api/tx',
            json={
                'subscriber_email': email,
                'template_id': WELCOME_TEMPLATE_ID,
                'data': {'name': name or email.split('@')[0]},
            },
            headers=_headers(),
            timeout=5,
        )
    except Exception:
        pass
