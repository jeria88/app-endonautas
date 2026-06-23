"""
Cliente de IA centralizado.

Uso:
    from config.ai_client import call_ai, user_intent_context
Todos los módulos deben llamar a call_ai() — nunca a la API directamente.

Orden de prioridad:
  1. AI_PROVIDER='openrouter'  → OpenRouter siempre
  2. AI_PROVIDER='deepseek'    → DeepSeek siempre
  3. AI_PROVIDER='auto'        → OpenRouter si hay OPENROUTER_API_KEY, si no DeepSeek
"""
import requests
from django.conf import settings


_PRIORITY_LABELS = {
    'propio':   'desarrollo personal propio',
    'familia':  'desarrollo de su familia',
    'negocio':  'desarrollo de su negocio',
    'carrera':  'desarrollo de su carrera profesional',
    'colectiva':'desarrollo de la conciencia colectiva',
}


def user_intent_context(user):
    """
    Devuelve un bloque de contexto para inyectar al inicio del system prompt.
    Vacío si el usuario no completó el onboarding o no tiene prioridades.
    """
    try:
        priorities = user.userprofile.onboarding_priorities or []
        if not priorities:
            return ''
        lines = '\n'.join(
            f'{i+1}. {_PRIORITY_LABELS.get(p, p)}'
            for i, p in enumerate(priorities)
        )
        return (
            f'Contexto del usuario:\n'
            f'Sus propósitos con el autoconocimiento, en orden de prioridad:\n'
            f'{lines}\n\n'
            f'Habla desde este contexto sin mencionarlo explícitamente.\n\n'
        )
    except Exception:
        return ''


def user_history_context(user):
    """
    Recopila historial del usuario (tests, sesión anterior del Espejo, bitácora,
    lecturas de nacimiento) para inyectar como contexto acumulado al Espejo.
    Cada sección falla silenciosamente si el modelo no está disponible.
    """
    sections = []

    # Tests psicométricos recientes con insight IA
    try:
        from psychometrics.models import TestResult
        results = (
            TestResult.objects
            .filter(user=user)
            .exclude(ai_insight='')
            .select_related('test')
            .order_by('-completed_at')[:5]
        )
        if results:
            items = [f'- {r.test.name}: {r.ai_insight[:200]}' for r in results]
            sections.append('Resultados psicométricos recientes:\n' + '\n'.join(items))
    except Exception:
        pass

    # Sesión Espejo anterior (conflict_summary + return_question)
    try:
        from mirror.models import ChatSession
        prev = (
            ChatSession.objects
            .filter(user=user)
            .exclude(conflict_summary='')
            .order_by('-updated_at')
            .first()
        )
        if prev:
            parts = []
            if prev.conflict_summary:
                parts.append(f'Conflicto trabajado: {prev.conflict_summary[:300]}')
            if prev.return_question:
                parts.append(f'Pregunta que quedó abierta: {prev.return_question}')
            if parts:
                sections.append('Sesión anterior del Espejo:\n' + '\n'.join(parts))
    except Exception:
        pass

    # Bitácora manual reciente
    try:
        from mirror.models import BitacoraEntry
        entries = (
            BitacoraEntry.objects
            .filter(user=user, entry_type__in=['sueno', 'sombra', 'patron', 'signo', 'manual'])
            .order_by('-created_at')[:5]
        )
        if entries:
            items = [f'- [{e.entry_type}] {e.content[:120]}' for e in entries]
            sections.append('Bitácora reciente:\n' + '\n'.join(items))
    except Exception:
        pass

    # Lectura de nacimiento (la primera disponible como referencia de carácter)
    try:
        from birth.models import BirthReport
        report = (
            BirthReport.objects
            .filter(birth_data__user=user, status='done')
            .exclude(ai_reading='')
            .order_by('report_type')
            .first()
        )
        if report:
            sections.append(
                f'Mapa de nacimiento ({report.report_type}):\n{report.ai_reading[:300]}'
            )
    except Exception:
        pass

    if not sections:
        return ''

    return (
        'Contexto acumulado del usuario (úsalo para acompañar con mayor profundidad; '
        'no lo menciones directamente a menos que el usuario lo traiga):\n\n'
        + '\n\n'.join(sections)
        + '\n\n'
    )


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
                'model': getattr(settings, 'OPENROUTER_MODEL', 'google/gemma-4-31b-it:free'),
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
