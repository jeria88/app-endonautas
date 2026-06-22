from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Comment, Forum, ForumPost, ForumReply, Post, Reaction

BUG_TYPES = [
    ('fractones_consumo', 'Consumo incorrecto de fractones'),
    ('fractones_carga', 'Fractones no acreditados'),
    ('pago', 'Error en pago o suscripción'),
    ('modulo', 'Fallo en un módulo'),
    ('otro', 'Otro'),
]

MODULES = [
    ('espejo', 'Espejo de Conflictos'),
    ('nacimiento', 'Lecturas de Nacimiento'),
    ('tests', 'Tests Psicométricos'),
    ('oraculo', 'Oráculo'),
    ('comunidad', 'Comunidad'),
    ('perfil', 'Perfil / Cuenta'),
    ('regulacion', 'Regulación'),
    ('otro', 'Otro'),
]


@login_required
def feed(request):
    posts = Post.objects.select_related('author__profile').prefetch_related('reactions', 'comments')[:30]
    return render(request, 'community/feed.html', {'posts': posts})


@login_required
def post_create(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            post = Post.objects.create(
                author=request.user,
                content=content,
                somatic_tag=request.POST.get('somatic_tag', ''),
            )
            if request.FILES.get('image'):
                post.image = request.FILES['image']
                post.save(update_fields=['image'])
            if request.FILES.get('video'):
                post.video = request.FILES['video']
                post.save(update_fields=['video'])
        return redirect('community_feed')
    return render(request, 'community/post_create.html')


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
        return redirect('community_post_detail', pk=pk)
    return render(request, 'community/post_detail.html', {'post': post})


@login_required
def share_create(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        shared_type = request.POST.get('shared_from_type', '')
        shared_id = request.POST.get('shared_from_id', '')
        shared_data = {}
        try:
            import json
            shared_data = json.loads(request.POST.get('shared_data', '{}'))
        except Exception:
            pass
        if content or shared_type:
            Post.objects.create(
                author=request.user,
                content=content or f'Compartí desde {shared_type}',
                shared_from_type=shared_type,
                shared_from_id=int(shared_id) if shared_id.isdigit() else None,
                shared_data=shared_data,
                somatic_tag=request.POST.get('somatic_tag', ''),
            )
    return redirect('community_feed')


@login_required
def foros(request):
    forums = Forum.objects.all()
    return render(request, 'community/foros.html', {'forums': forums})


@login_required
def forum_detail(request, slug):
    forum = get_object_or_404(Forum, slug=slug)
    posts = forum.posts.select_related('author__profile').prefetch_related('replies')
    return render(request, 'community/forum_detail.html', {
        'forum': forum,
        'posts': posts,
    })


@login_required
def forum_post_create(request, slug):
    forum = get_object_or_404(Forum, slug=slug)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if not title:
            return render(request, 'community/forum_post_create.html', {
                'forum': forum, 'bug_types': BUG_TYPES, 'modules': MODULES,
                'error': 'El título es obligatorio.',
                'prev': request.POST,
            })

        structured = {}
        if forum.is_bug_forum:
            structured = {
                'bug_type': request.POST.get('bug_type', ''),
                'module': request.POST.get('module', ''),
                'steps': request.POST.get('steps', '').strip(),
                'expected': request.POST.get('expected', '').strip(),
                'actual': request.POST.get('actual', '').strip(),
            }

        post = ForumPost.objects.create(
            forum=forum,
            author=request.user,
            title=title,
            content=content,
            structured_data=structured,
        )
        return redirect('forum_post_detail', slug=slug, pk=post.pk)

    return render(request, 'community/forum_post_create.html', {
        'forum': forum,
        'bug_types': BUG_TYPES,
        'modules': MODULES,
    })


@login_required
def forum_post_detail(request, slug, pk):
    forum = get_object_or_404(Forum, slug=slug)
    post = get_object_or_404(ForumPost, pk=pk, forum=forum)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            ForumReply.objects.create(post=post, author=request.user, content=content)
        return redirect('forum_post_detail', slug=slug, pk=pk)

    replies = post.replies.select_related('author__profile')
    bug_type_label = ''
    if post.structured_data.get('bug_type'):
        bug_type_label = dict(BUG_TYPES).get(post.structured_data['bug_type'], '')
    module_label = ''
    if post.structured_data.get('module'):
        module_label = dict(MODULES).get(post.structured_data['module'], '')

    return render(request, 'community/forum_post_detail.html', {
        'forum': forum,
        'post': post,
        'replies': replies,
        'bug_type_label': bug_type_label,
        'module_label': module_label,
    })


@login_required
def mensajes(request):
    return render(request, 'community/mensajes.html')


@login_required
@require_POST
def post_react(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reaction_type = request.POST.get('type', 'resonar')
    reaction, created = Reaction.objects.get_or_create(
        post=post, user=request.user, defaults={'reaction_type': reaction_type}
    )
    if not created:
        reaction.delete()
        post.score -= 1
    else:
        post.score += 1
    post.save(update_fields=['score'])
    return JsonResponse({'score': post.score, 'active': created})
