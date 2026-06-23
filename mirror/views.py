import datetime
import math

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import BitacoraEntry, CategoriaNecesidad, ChatMessage, ChatSession, DreamEntry, EjercicioRegulacion, MomentoRegulacion


@login_required
def espejo_home(request):
    sessions = ChatSession.objects.filter(user=request.user).prefetch_related('messages').order_by('-updated_at')[:20]
    return render(request, 'mirror/home.html', {'sessions': sessions})


@login_required
def chat_new(request):
    from accounts.plan_utils import plan_at_least
    from django.utils import timezone
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not plan_at_least(request.user, 'navegante'):
        today = timezone.now().date()
        existing = ChatSession.objects.filter(user=request.user, created_at__date=today).first()
        if existing:
            if is_ajax:
                return JsonResponse({'pk': existing.pk, 'title': existing.title or 'Tu sesión de hoy', 'reused': True})
            return redirect('espejo_chat', pk=existing.pk)
    session = ChatSession.objects.create(user=request.user)
    if is_ajax:
        return JsonResponse({'pk': session.pk, 'title': session.title or 'Nueva conversación'})
    return redirect('espejo_chat', pk=session.pk)


@login_required
def chat_session(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    return render(request, 'mirror/chat.html', {'session': session})


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
    from accounts.plan_utils import plan_at_least
    from django.utils import timezone
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    if not plan_at_least(request.user, 'navegante'):
        age = timezone.now() - session.created_at
        if age > datetime.timedelta(minutes=45):
            return JsonResponse({
                'error': 'Tu sesión de hoy ha alcanzado el límite de 45 minutos. Actualiza al plan Navegante para sesiones sin límite.',
                'upgrade_required': True,
            }, status=403)
    content = request.POST.get('content', '').strip()
    file = request.FILES.get('attachment')
    if not content and not file:
        return JsonResponse({'error': 'Mensaje vacío'}, status=400)

    # Determinar tipo de adjunto
    att_type = ''
    if file:
        ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
        if ext in ('jpg', 'jpeg', 'png', 'webp'):
            att_type = 'image'
        elif ext == 'pdf':
            att_type = 'pdf'
        elif ext in ('doc', 'docx'):
            att_type = 'doc'

    user_msg = ChatMessage(session=session, role='user', content=content or '')
    if file and att_type:
        user_msg.attachment = file
        user_msg.attachment_type = att_type
    user_msg.save()

    new_title = None
    title_src = content or (file.name if file else '')
    if not session.title and title_src:
        session.title = title_src[:60].strip()
        session.save(update_fields=['title'])
        new_title = session.title

    # Pasar adjunto abierto a _get_reply si es necesario
    att_file = user_msg.attachment if att_type else None
    reply = _get_reply(session, content, user=request.user, attachment=att_file, attachment_type=att_type)
    msg = ChatMessage.objects.create(session=session, role='assistant', content=reply)

    resp = {'reply': reply, 'created_at': msg.created_at.isoformat()}
    if new_title:
        resp['title'] = new_title
    if att_type:
        resp['attachment_url'] = user_msg.attachment.url if user_msg.attachment else ''
        resp['attachment_type'] = att_type
        resp['attachment_name'] = file.name if file else ''
    return JsonResponse(resp)


@login_required
def regulacion(request):
    import json

    momentos_qs = MomentoRegulacion.objects.filter(activo=True).prefetch_related(
        'categorias', 'momentoejercicio_set__ejercicio'
    )
    categorias_qs = CategoriaNecesidad.objects.all()

    momentos_json = [m.as_json() for m in momentos_qs]
    categorias_json = [
        {'slug': c.slug, 'nombre': c.nombre, 'tipo': c.tipo}
        for c in categorias_qs
    ]

    return render(request, 'mirror/regulacion.html', {
        'momentos_json': json.dumps(momentos_json, ensure_ascii=False),
        'categorias_json': json.dumps(categorias_json, ensure_ascii=False),
        'total': momentos_qs.count(),
    })


@login_required
def regulacion_api(request):
    """Endpoint para otros módulos — sugiere ejercicios por estado o categoría."""
    categoria = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')
    limit = min(int(request.GET.get('limit', 3)), 10)

    qs = EjercicioRegulacion.objects.filter(active=True)
    if categoria:
        qs = qs.filter(category=categoria)
    if estado:
        qs = [e for e in qs if estado in (e.emotional_targets or [])]
    else:
        qs = list(qs)

    import random
    sample = random.sample(qs, min(limit, len(qs)))
    return JsonResponse({
        'ejercicios': [e.as_json() for e in sample]
    })


@login_required
@require_POST
def regulacion_completado(request):
    import json
    try:
        data = json.loads(request.body)
        ejercicio_id = data.get('ejercicio_id')
        ejercicio = EjercicioRegulacion.objects.get(pk=ejercicio_id, active=True)
        BitacoraEntry.objects.create(
            user=request.user,
            entry_type='auto_regulacion',
            content=f'Ejercicio completado: {ejercicio.title} ({ejercicio.get_category_display()})',
            meta={'ejercicio_id': ejercicio.pk, 'categoria': ejercicio.category, 'ui_mode': ejercicio.ui_mode},
        )
    except Exception:
        pass
    return JsonResponse({'ok': True})


@login_required
def suenos_list(request):
    return redirect('bitacora_list')


@login_required
def sueno_create(request):
    return redirect('/bitacora/nueva/?tipo=sueno')


# ── Bitácora ──────────────────────────────────────────────────────────────────

MANUAL_TYPES = ('sueno', 'sombra', 'patron', 'signo', 'manual')
CATEGORY_LABELS = {
    'sueno': 'Sueños',
    'sombra': 'Sombras',
    'patron': 'Patrones',
    'signo': 'Signos y Síntomas',
    'manual': 'Notas libres',
}

@login_required
def bitacora_list(request):
    tab = request.GET.get('tab', '')
    qs = BitacoraEntry.objects.filter(user=request.user).order_by('-created_at')
    if tab in MANUAL_TYPES:
        qs = qs.filter(entry_type=tab)
    elif tab == 'actividad':
        qs = qs.exclude(entry_type__in=MANUAL_TYPES)
    return render(request, 'mirror/bitacora_list.html', {
        'entries': qs,
        'tab': tab,
        'category_labels': CATEGORY_LABELS,
    })


_EMOCIONES = ['miedo', 'ira', 'verguenza', 'culpa', 'tristeza', 'envidia', 'ansiedad', 'asco', 'celos']


def _parse_meta(post, entry_type):
    meta = {}
    if entry_type == 'sueno':
        meta['lucido']     = 'lucido' in post
        meta['recurrente'] = 'recurrente' in post
        meta['pesadilla']  = 'pesadilla' in post
        meta['personajes'] = post.get('personajes', '').strip()
        meta['ambiente']   = post.get('ambiente', '').strip()
    elif entry_type == 'sombra':
        meta['conflicto'] = post.get('conflicto', '').strip()
        meta['figura']    = post.get('figura', '').strip()
        checked = set(post.getlist('emo_checked'))
        meta['emociones'] = [
            {'nombre': emo, 'procesamiento': post.get(f'emo_proc_{emo}', '')}
            for emo in _EMOCIONES if emo in checked
        ]
    elif entry_type == 'patron':
        meta['detonante']  = post.get('detonante', '').strip()
        meta['frecuencia'] = post.get('frecuencia', '')
        meta['area_vital'] = post.getlist('area_vital')
        meta['cambiar']    = 'cambiar' in post
    elif entry_type == 'signo':
        meta['ubicacion']  = post.get('ubicacion', '').strip()
        intensidad = post.get('intensidad_signo', '')
        meta['intensidad'] = int(intensidad) if intensidad.isdigit() else None
        meta['momento']    = post.getlist('momento')
        meta['detonante']  = post.get('detonante', '').strip()
    return meta


@login_required
def bitacora_create(request):
    tipo_default = request.GET.get('tipo', 'manual')
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        entry_type = request.POST.get('entry_type', 'manual')
        if entry_type not in [t[0] for t in BitacoraEntry.ENTRY_TYPES]:
            entry_type = 'manual'
        if content:
            BitacoraEntry.objects.create(
                user=request.user,
                entry_type=entry_type,
                content=content,
                tags=request.POST.get('tags', '').strip(),
                emoji=request.POST.get('emoji', '').strip()[:2],
                meta=_parse_meta(request.POST, entry_type),
            )
        return redirect('bitacora_list')
    return render(request, 'mirror/bitacora_form.html', {
        'tipo_default': tipo_default,
        'manual_types': MANUAL_TYPES,
    })


@login_required
def bitacora_edit(request, pk):
    entry = get_object_or_404(BitacoraEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        entry_type = request.POST.get('entry_type', entry.entry_type)
        if entry_type not in [t[0] for t in BitacoraEntry.ENTRY_TYPES]:
            entry_type = entry.entry_type
        if content:
            entry.content = content
            entry.entry_type = entry_type
            entry.tags = request.POST.get('tags', '').strip()
            entry.emoji = request.POST.get('emoji', '').strip()[:2]
            entry.meta = _parse_meta(request.POST, entry_type)
            entry.save()
        return redirect('bitacora_list')
    return render(request, 'mirror/bitacora_form.html', {
        'entry': entry,
        'tipo_default': entry.entry_type,
        'manual_types': MANUAL_TYPES,
        'editing': True,
    })


@login_required
def bitacora_delete(request, pk):
    entry = get_object_or_404(BitacoraEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
    return redirect('bitacora_list')


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


def _cosine(a, b):
    n = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b)) / n if n else 0.0


def _retrieve_context(query, k=5):
    from mirror.models import KnowledgeChunk
    chunks = KnowledgeChunk.objects.all()
    if not chunks.exists():
        return []
    # Retrieval semántico si hay embeddings disponibles
    with_emb = chunks.exclude(embedding=[])
    if with_emb.exists():
        try:
            from config.ai_client import get_embedding
            q_vec = get_embedding(query)
            if q_vec:
                scored = sorted(
                    [(c, _cosine(q_vec, c.embedding)) for c in with_emb],
                    key=lambda x: x[1], reverse=True,
                )
                return [c.content for c, _ in scored[:k]]
        except Exception:
            pass
    # Fallback: búsqueda por palabras clave
    words = [w for w in query.lower().split() if len(w) > 3]
    if not words:
        return []
    from django.db.models import Q
    q = Q()
    for w in words[:5]:
        q |= Q(content__icontains=w)
    return list(chunks.filter(q).values_list('content', flat=True)[:k])


def _extract_attachment_text(file_field, attachment_type):
    """Extrae texto de un adjunto PDF o doc. Retorna (texto, mime_base64) según tipo."""
    if not file_field:
        return None, None, None
    try:
        if attachment_type == 'image':
            import base64
            file_field.seek(0)
            data = file_field.read()
            b64 = base64.b64encode(data).decode()
            ext = file_field.name.rsplit('.', 1)[-1].lower()
            mime = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}.get(ext, 'image/jpeg')
            return None, b64, mime
        elif attachment_type == 'pdf':
            import PyPDF2
            file_field.seek(0)
            reader = PyPDF2.PdfReader(file_field)
            text = '\n\n'.join(p.extract_text() or '' for p in reader.pages)
            return text[:4000], None, None
        elif attachment_type == 'doc':
            import docx
            import io
            file_field.seek(0)
            doc = docx.Document(io.BytesIO(file_field.read()))
            text = '\n'.join(p.text for p in doc.paragraphs if p.text.strip())
            return text[:4000], None, None
    except Exception:
        pass
    return None, None, None


def _get_reply(session, user_content, user=None, attachment=None, attachment_type=None):
    from config.ai_client import call_ai, user_intent_context, user_history_context
    intent = user_intent_context(user) if user else ''
    history_ctx = user_history_context(user) if user else ''
    query = user_content or ''
    kb_chunks = _retrieve_context(query, k=5) if query else []
    kb_text = ''
    if kb_chunks:
        kb_text = (
            'Marco teórico de referencia (úsalo si es pertinente; no lo cites textualmente):\n'
            + '\n\n---\n\n'.join(kb_chunks)
            + '\n\n'
        )
    system = intent + history_ctx + kb_text + _load_system_prompt()
    history = list(session.messages.values('role', 'content'))
    messages = [{'role': 'system', 'content': system}]
    messages += [{'role': m['role'] if m['role'] == 'user' else 'assistant', 'content': m['content']} for m in history[-10:]]

    # Construir mensaje del usuario según tipo de adjunto
    extra_text, img_b64, img_mime = _extract_attachment_text(attachment, attachment_type)
    if img_b64:
        user_part = {'role': 'user', 'content': [
            {'type': 'text', 'text': user_content or 'Observa esta imagen y comparte lo que ves.'},
            {'type': 'image_url', 'image_url': {'url': f'data:{img_mime};base64,{img_b64}'}},
        ]}
    elif extra_text:
        combined = f'{user_content}\n\n[Documento adjunto]:\n{extra_text}' if user_content else f'[Documento adjunto]:\n{extra_text}'
        user_part = {'role': 'user', 'content': combined}
    else:
        user_part = {'role': 'user', 'content': user_content}

    messages.append(user_part)
    return call_ai(messages, max_tokens=700) or 'No pude conectar con el espejo en este momento.'


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
