"""
Cliente de IA centralizado.
Todos los módulos deben llamar a call_ai() — nunca a la API directamente.

Orden de prioridad:
  1. AI_PROVIDER='openrouter'  → OpenRouter siempre
  2. AI_PROVIDER='deepseek'    → DeepSeek siempre
  3. AI_PROVIDER='auto'        → OpenRouter si hay OPENROUTER_API_KEY, si no DeepSeek
"""
import requests
from django.conf import settings


def call_ai(messages, max_tokens=500, timeout=25):
    """
    Llama al proveedor de IA configurado.

    Args:
        messages: lista de dicts {role, content} — formato OpenAI estándar
        max_tokens: límite de tokens en la respuesta
        timeout: segundos antes de abortar

    Returns:
        str — texto de la respuesta, o '' si falla
    """
    provider = _resolve_provider()
    if provider == 'openrouter':
        return _call_openrouter(messages, max_tokens, timeout)
    if provider == 'deepseek':
        return _call_deepseek(messages, max_tokens, timeout)
    return ''


def _resolve_provider():
    setting = getattr(settings, 'AI_PROVIDER', 'auto')
    if setting == 'openrouter':
        return 'openrouter' if getattr(settings, 'OPENROUTER_API_KEY', '') else ''
    if setting == 'deepseek':
        return 'deepseek' if getattr(settings, 'DEEPSEEK_API_KEY', '') else ''
    # auto: openrouter tiene prioridad sobre deepseek
    if getattr(settings, 'OPENROUTER_API_KEY', ''):
        return 'openrouter'
    if getattr(settings, 'DEEPSEEK_API_KEY', ''):
        return 'deepseek'
    return ''


def _call_openrouter(messages, max_tokens, timeout):
    try:
        r = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            json={
                'model': getattr(settings, 'OPENROUTER_MODEL', 'meta-llama/llama-3.1-8b-instruct:free'),
                'messages': messages,
                'max_tokens': max_tokens,
            },
            headers={'Authorization': f'Bearer {settings.OPENROUTER_API_KEY}'},
            timeout=timeout,
        )
        return r.json()['choices'][0]['message']['content']
    except Exception:
        return ''


def _call_deepseek(messages, max_tokens, timeout):
    try:
        r = requests.post(
            'https://api.deepseek.com/chat/completions',
            json={
                'model': getattr(settings, 'DEEPSEEK_MODEL', 'deepseek-chat'),
                'messages': messages,
                'max_tokens': max_tokens,
            },
            headers={'Authorization': f'Bearer {settings.DEEPSEEK_API_KEY}'},
            timeout=timeout,
        )
        return r.json()['choices'][0]['message']['content']
    except Exception:
        return ''
