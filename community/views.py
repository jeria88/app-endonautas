from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Comment, Post, Reaction


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
                post.save()
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
def foros(request):
    return render(request, 'community/foros.html')


@login_required
def mensajes(request):
    return render(request, 'community/mensajes.html')


@login_required
@require_POST
def post_react(request, pk):
    from django.http import JsonResponse
    post = get_object_or_404(Post, pk=pk)
    reaction_type = request.POST.get('type', 'resonar')
    reaction, created = Reaction.objects.get_or_create(post=post, user=request.user, defaults={'reaction_type': reaction_type})
    if not created:
        reaction.delete()
        post.score -= 1
    else:
        post.score += 1
    post.save()
    return JsonResponse({'score': post.score, 'active': created})
