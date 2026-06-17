import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import BitacoraEntry, ChatMessage, ChatSession, DreamEntry, EjercicioRegulacion


def _get_token_balance(user):
    if user.is_superuser:
        return '∞'
    try:
        from tokens.models import TokenBalance
        return TokenBalance.objects.get(user=user).balance
    except Exception:
        return 0


@login_required
def espejo_home(request):
    sessions = ChatSession.objects.filter(user=request.user).prefetch_related('messages').order_by('-updated_at')[:20]
    return render(request, 'mirror/home.html', {
        'sessions': sessions,
        'token_balance': _get_token_balance(request.user),
    })


@login_required
def chat_new(request):
    from tokens.service import has_balance
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not request.user.is_superuser and not has_balance(request.user, 'espejo_exchange'):
        if is_ajax:
            return JsonResponse({'error': 'sin_fractones', 'redirect': '/tokens/'}, status=402)
        return redirect('tokens_balance')
    session = ChatSession.objects.create(user=request.user)
    if is_ajax:
        return JsonResponse({'pk': session.pk, 'title': session.title or 'Nueva conversación'})
    return redirect('espejo_chat', pk=session.pk)


@login_required
def chat_session(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    return render(request, 'mirror/chat.html', {
        'session': session,
        'token_balance': _get_token_balance(request.user),
    })


@login_required
def chat_session_api(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    messages = [
        {'role': m.role, 'content': m.content, 'created_at': m.created_at.strftime('%H:%M')}
        for m in session.messages.all()
    ]
    return JsonResponse({'pk': session.pk, 'title': session.title or 'Conversación', 'messages': messages})


@login_required
@require_POST
def chat_message(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    from tokens.service import spend
    if not request.user.is_superuser and not spend(request.user, 'espejo_exchange'):
        return JsonResponse({'error': 'Sin fractones'}, status=402)

    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'error': 'Mensaje vacío'}, status=400)

    ChatMessage.objects.create(session=session, role='user', content=content)
    reply = _get_reply(session, content)
    msg = ChatMessage.objects.create(session=session, role='assistant', content=reply)

    from tokens.service import credit_mission
    credit_mission(request.user, 'first_espejo')

    return JsonResponse({'reply': reply, 'created_at': msg.created_at.isoformat()})


@login_required
def regulacion(request):
    ejercicios = EjercicioRegulacion.objects.filter(active=True).order_by('order')
    return render(request, 'mirror/regulacion.html', {'ejercicios': ejercicios})


@login_required
def suenos_list(request):
    entries = DreamEntry.objects.filter(user=request.user)
    return render(request, 'mirror/suenos_list.html', {'entries': entries})


@login_required
def sueno_create(request):
    if request.method == 'POST':
        entry = DreamEntry.objects.create(
            user=request.user,
            title=request.POST.get('title', '').strip(),
            content=request.POST.get('content', '').strip(),
            is_lucid='is_lucid' in request.POST,
            reality_check='reality_check' in request.POST,
            dream_date=request.POST.get('dream_date') or datetime.date.today(),
            tags=request.POST.get('tags', '').strip(),
        )
        BitacoraEntry.objects.create(
            user=request.user,
            entry_type='auto_dream',
            content=f'Registré un sueño: {entry.title or "Sin título"}',
            emoji='◈',
        )
        return redirect('suenos_list')
    return render(request, 'mirror/sueno_form.html', {'today': datetime.date.today()})


# ── Bitácora ──────────────────────────────────────────────────────────────────

@login_required
def bitacora_list(request):
    entries = BitacoraEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'mirror/bitacora_list.html', {'entries': entries})


@login_required
def bitacora_create(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            BitacoraEntry.objects.create(
                user=request.user,
                entry_type='manual',
                content=content,
                tags=request.POST.get('tags', '').strip(),
                emoji=request.POST.get('emoji', '').strip()[:2],
            )
        return redirect('bitacora_list')
    return render(request, 'mirror/bitacora_form.html')


@login_required
def bitacora_delete(request, pk):
    entry = get_object_or_404(BitacoraEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
    return redirect('bitacora_list')


# ── Nauminto ──────────────────────────────────────────────────────────────────

@login_required
def nauminto_list(request):
    entries = DreamEntry.objects.filter(user=request.user, is_nauminto=True).order_by('-dream_date')
    return render(request, 'mirror/nauminto_list.html', {'entries': entries})


@login_required
def nauminto_create(request):
    if request.method == 'POST':
        archetypes = request.POST.getlist('archetypes')
        entry = DreamEntry.objects.create(
            user=request.user,
            title=request.POST.get('title', '').strip(),
            content=request.POST.get('content', '').strip(),
            dream_date=request.POST.get('dream_date') or datetime.date.today(),
            nauminto_type=request.POST.get('nauminto_type', ''),
            archetype_tags=archetypes,
            tags=request.POST.get('tags', '').strip(),
            is_nauminto=True,
        )
        BitacoraEntry.objects.create(
            user=request.user,
            entry_type='auto_dream',
            content=f'Nauminto registrado: {entry.title or "Sin título"}',
            emoji='✦',
        )
        return redirect('nauminto_list')
    return render(request, 'mirror/nauminto_form.html', {'today': datetime.date.today()})


@login_required
def nauminto_detail(request, pk):
    entry = get_object_or_404(DreamEntry, pk=pk, user=request.user, is_nauminto=True)
    return render(request, 'mirror/nauminto_detail.html', {'entry': entry})


@login_required
def sueno_detail(request, pk):
    entry = get_object_or_404(DreamEntry, pk=pk, user=request.user)
    return render(request, 'mirror/sueno_detail.html', {'entry': entry})


def _load_system_prompt():
    import os
    path = os.path.join(os.path.dirname(__file__), 'prompts', 'espejo_system.txt')
    try:
        with open(path, encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return 'Eres el Espejo de Conflictos, un acompañante de autoconocimiento.'


def _get_reply(session, user_content):
    import requests
    from django.conf import settings
    if not settings.DEEPSEEK_API_KEY:
        return 'El espejo no puede responder ahora (configura DEEPSEEK_API_KEY).'

    history = list(session.messages.values('role', 'content'))
    messages = [{'role': 'system', 'content': _load_system_prompt()}]
    messages += [{'role': m['role'] if m['role'] == 'user' else 'assistant', 'content': m['content']} for m in history[-10:]]
    messages.append({'role': 'user', 'content': user_content})

    try:
        r = requests.post(
            'https://api.deepseek.com/chat/completions',
            json={'model': settings.DEEPSEEK_MODEL, 'messages': messages, 'max_tokens': 500},
            headers={'Authorization': f'Bearer {settings.DEEPSEEK_API_KEY}'},
            timeout=25,
        )
        return r.json()['choices'][0]['message']['content']
    except Exception:
        return 'No pude conectar con el espejo en este momento.'


@login_required
@require_POST
def chat_session_rename(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    title = request.POST.get('title', '').strip()[:200]
    if title:
        session.title = title
        session.save(update_fields=['title'])
    return JsonResponse({'ok': True, 'title': session.title})


@login_required
@require_POST
def chat_session_delete(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    session.delete()
    return JsonResponse({'ok': True})


@login_required
def chat_session_export(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    messages = session.messages.all().order_by('created_at')
    lines = [
        f'# {session.title or "Conversación"}',
        f'Exportado: {datetime.date.today()}',
        '',
    ]
    for m in messages:
        label = 'Tú' if m.role == 'user' else 'Espejo'
        lines.append(f'[{m.created_at.strftime("%H:%M")}] {label}:')
        lines.append(m.content)
        lines.append('')
    content = '\n'.join(lines)
    filename = (session.title or 'conversacion').replace(' ', '_')[:60]
    response = HttpResponse(content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}.txt"'
    return response
