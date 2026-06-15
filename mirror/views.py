from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import ChatMessage, ChatSession


@login_required
def espejo_home(request):
    sessions = ChatSession.objects.filter(user=request.user)[:10]
    return render(request, 'mirror/home.html', {'sessions': sessions})


@login_required
def chat_new(request):
    from tokens.service import has_balance, spend
    if not has_balance(request.user, 'espejo_exchange'):
        return redirect('tokens_balance')
    session = ChatSession.objects.create(user=request.user)
    return redirect('espejo_chat', pk=session.pk)


@login_required
def chat_session(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    return render(request, 'mirror/chat.html', {'session': session})


@login_required
@require_POST
def chat_message(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    from tokens.service import spend
    if not spend(request.user, 'espejo_exchange'):
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


def _get_reply(session, user_content):
    import requests
    from django.conf import settings
    if not settings.DEEPSEEK_API_KEY:
        return 'El espejo no puede responder ahora (configura DEEPSEEK_API_KEY).'

    history = list(session.messages.values('role', 'content'))
    messages = [{'role': 'system', 'content': 'Eres el Espejo de Conflictos, un acompañante de autoconocimiento.'}]
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
