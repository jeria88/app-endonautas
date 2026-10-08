"""Avisos al harness de ACME Agents (CRM + bus de eventos del tenant endonautas).

La app sigue siendo dueña del funnel del ebook; esto solo le cuenta al núcleo lo que pasó
(lead, checkout, venta) para que el CRM y el embudo de la marca estén completos.
Plan: ~/plans/acmeagents/2026-10-08-business-harness-rework.md (etapa 1, integración por eventos).

Reglas: sin HARNESS_API_KEY es no-op; nunca bloquea ni rompe el request (hilo aparte, timeout
corto, todo en try/except). El harness deduplica por `dedupe_key`, así que reintentar es seguro.
"""
import logging
import os
import threading
from decimal import Decimal

import requests

logger = logging.getLogger(__name__)

HARNESS_URL = os.environ.get('HARNESS_URL', 'https://api.acmeagents.team/api/harness/events')
# Solo para convertir ventas en USD a una cifra comparable en el embudo; el monto original
# viaja igual en `datos`. No es contabilidad.
USD_CLP = int(os.environ.get('HARNESS_USD_CLP', '950'))


def a_clp(amount, currency) -> int:
    amount = Decimal(str(amount))
    if (currency or '').upper() == 'CLP':
        return int(amount)
    return int(round(amount * USD_CLP))


def _post(payload: dict, api_key: str) -> None:
    try:
        r = requests.post(HARNESS_URL, json=payload, timeout=4,
                          headers={'Authorization': f'Bearer {api_key}'})
        if r.status_code >= 400:
            logger.warning('harness %s → %s %s', payload.get('tipo'), r.status_code, r.text[:200])
    except Exception as e:  # el harness caído no puede costar una venta ni un lead
        logger.warning('harness %s no enviado: %s', payload.get('tipo'), e)


def emitir(tipo: str, contacto: dict, *, datos: dict = None, monto_clp: int = None,
           dedupe_key: str = None, atribucion: str = None, sync: bool = False) -> bool:
    """Encola el aviso. Devuelve False si no hay API key configurada (no-op)."""
    api_key = os.environ.get('HARNESS_API_KEY', '')
    if not api_key:
        return False
    payload = {
        'tipo': tipo,
        'contacto': {k: v for k, v in contacto.items() if v not in (None, '')},
        'datos': datos or {},
        'monto_clp': monto_clp,
        'dedupe_key': dedupe_key,
        'departamento': 'externo',
        'rol': 'app-endonautas',
        'atribucion': atribucion,
    }
    if sync:
        _post(payload, api_key)
    else:
        threading.Thread(target=_post, args=(payload, api_key), daemon=True).start()
    return True
