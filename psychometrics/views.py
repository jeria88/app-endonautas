from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Test, TestResult


def test_list(request):
    tests = Test.objects.filter(active=True).order_by('dimension', 'order')
    by_dimension = {}
    for t in tests:
        by_dimension.setdefault(t.get_dimension_display(), []).append(t)
    return render(request, 'psychometrics/test_list.html', {'by_dimension': by_dimension})


def test_detail(request, slug):
    test = get_object_or_404(Test, slug=slug, active=True)
    return render(request, 'psychometrics/test_detail.html', {'test': test})


@login_required
def test_take(request, slug):
    test = get_object_or_404(Test, slug=slug, active=True)
    questions = test.questions.all()

    if request.method == 'POST':
        raw_scores = {}
        dim_scores = {}
        for q in questions:
            val = request.POST.get(f'q_{q.pk}')
            if val is not None:
                score = int(val)
                if q.reverse_scored:
                    score = _reverse(score, q.scale)
                raw_scores[str(q.pk)] = score
                key = q.dimension_key or 'total'
                dim_scores[key] = dim_scores.get(key, 0) + score

        from psychometrics.evaluator import evaluate_test
        evaluation = evaluate_test(test.name, dim_scores)

        result = TestResult.objects.create(
            user=request.user,
            test=test,
            raw_scores=raw_scores,
            evaluation=evaluation,
        )
        return redirect('test_result', pk=result.pk)

    return render(request, 'psychometrics/test_take.html', {'test': test, 'questions': questions})


def _reverse(score, scale):
    if scale in ('likert5', 'likert5a'):
        return 6 - score
    if scale == 'likert4':
        return 4 - score
    if scale == 'likert3':
        return 3 - score
    if scale == 'likert7':
        return 8 - score
    if scale == 'binary':
        return 1 - score
    return score


@login_required
def test_result(request, pk):
    result = get_object_or_404(TestResult, pk=pk, user=request.user)

    if not result.ai_insight and request.GET.get('ai'):
        from tokens.service import has_balance, spend
        if has_balance(request.user, 'ai_insight') and spend(request.user, 'ai_insight'):
            result.ai_insight = _generate_insight(result)
            result.save()

    return render(request, 'psychometrics/test_result.html', {'result': result})


def _generate_insight(result):
    import requests
    from django.conf import settings
    if not settings.DEEPSEEK_API_KEY:
        return ''
    payload = {
        'model': settings.DEEPSEEK_MODEL,
        'messages': [{'role': 'user', 'content': f'Dame un insight breve sobre este resultado: {result.evaluation}'}],
        'max_tokens': 300,
    }
    try:
        r = requests.post(
            'https://api.deepseek.com/chat/completions',
            json=payload,
            headers={'Authorization': f'Bearer {settings.DEEPSEEK_API_KEY}'},
            timeout=20,
        )
        return r.json()['choices'][0]['message']['content']
    except Exception:
        return ''


@login_required
def my_results(request):
    results = TestResult.objects.filter(user=request.user).select_related('test')
    return render(request, 'psychometrics/my_results.html', {'results': results})
