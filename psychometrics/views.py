import json

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Test, TestResult

DIMENSION_COLORS = {
    'identidad': '#7ECCCD',
    'emociones': '#c97b84',
    'cuerpo': '#7ec49b',
    'vinculos': '#d4a056',
    'sombra': '#9b8ec4',
    'espiritualidad': '#7ECCCD',
    'suenos': '#9b8ec4',
    'proposito': '#d4a056',
    'comunidad': '#7ec49b',
    'abundancia': '#d4a056',
    'creatividad': '#c97b84',
    'mente': '#7ECCCD',
}


def test_list(request):
    tests = cache.get('active_tests')
    if tests is None:
        tests = list(Test.objects.filter(active=True).order_by('dimension', 'order'))
        cache.set('active_tests', tests, 60 * 60)
    by_dimension = {}
    for t in tests:
        by_dimension.setdefault(t.get_dimension_display(), []).append(t)

    completed_slugs = set()
    if request.user.is_authenticated:
        completed_slugs = set(
            TestResult.objects.filter(user=request.user)
            .values_list('test__slug', flat=True)
        )
    return render(request, 'psychometrics/test_list.html', {
        'by_dimension': by_dimension, 'completed_slugs': completed_slugs
    })


def test_detail(request, slug):
    from accounts.plan_utils import FREE_TEST_SLUGS, plan_at_least, upgrade_wall
    test = get_object_or_404(Test, slug=slug, active=True)
    if request.user.is_authenticated and slug not in FREE_TEST_SLUGS and not plan_at_least(request.user, 'navegante'):
        return upgrade_wall(request, 'navegante', test.name)
    return render(request, 'psychometrics/test_detail.html', {'test': test})


@login_required
def test_take(request, slug):
    from accounts.plan_utils import FREE_TEST_SLUGS, plan_at_least, upgrade_wall
    test = get_object_or_404(Test, slug=slug, active=True)
    if slug not in FREE_TEST_SLUGS and not plan_at_least(request.user, 'navegante'):
        return upgrade_wall(request, 'navegante', test.name)
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
            user=request.user, test=test,
            raw_scores=raw_scores, evaluation=evaluation,
        )
        from mirror.models import BitacoraEntry
        BitacoraEntry.objects.create(
            user=request.user,
            entry_type='auto_test',
            content=f'Completé el test: {test.name}',
            emoji='◎',
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
        from accounts.plan_utils import plan_at_least
        if plan_at_least(request.user, 'navegante'):
            result.ai_insight = _generate_insight(result)
            result.save()

    return render(request, 'psychometrics/test_result.html', {'result': result})


@login_required
def test_result_pdf(request, pk):
    result = get_object_or_404(TestResult, pk=pk, user=request.user)
    return _generate_pdf(result)


def _generate_pdf(result):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = f'attachment; filename="resultado-{result.pk}.pdf"'

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2.5*cm, rightMargin=2.5*cm)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=20, spaceAfter=10)
    story.append(Paragraph(f'Resultado: {result.test.name}', title_style))
    story.append(Paragraph(f'Fecha: {result.completed_at.strftime("%d/%m/%Y")}', styles['Normal']))
    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph('Puntuaciones por dimensión', styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))

    table_data = [['Dimensión', 'Puntuación', 'Porcentaje']]
    dims = result.evaluation.get('dimensiones', [])
    for d in dims:
        nombre = d.get('nombre', '')
        puntos = d.get('puntos', 0)
        max_val = d.get('max', 0)
        pct = d.get('pct', 0)
        table_data.append([
            nombre,
            f"{round(puntos, 1)} / {round(max_val, 1)}",
            f"{round(pct, 1)}%"
        ])

    table = Table(table_data, colWidths=[9*cm, 3.5*cm, 3.5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7ECCCD')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(table)

    conclusion = result.evaluation.get('conclusion', '')
    if conclusion:
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph('Lectura Endonáutica', styles['Heading2']))
        story.append(Paragraph(conclusion, styles['Normal']))

    if result.ai_insight:
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph('Insight IA', styles['Heading2']))
        story.append(Paragraph(result.ai_insight, styles['Normal']))

    story.append(Spacer(1, 1*cm))
    story.append(Paragraph('Generado por Endonautas — endonautas.cl', styles['Normal']))

    doc.build(story)
    return buffer


@login_required
def test_result_share(request, pk):
    result = get_object_or_404(TestResult, pk=pk, user=request.user)
    if request.method == 'POST':
        from community.models import Post
        caption = request.POST.get('caption', '')
        eval_summary = []
        for k, v in result.evaluation.items():
            if isinstance(v, (int, float)):
                eval_summary.append(f'{k}: {round(v, 1)}')
        Post.objects.create(
            author=request.user,
            content=f'{caption}\n\nCompleté el test: {result.test.name}'.strip(),
            shared_from_type='test_result',
            shared_from_id=result.pk,
            shared_data={
                'test_name': result.test.name,
                'dimension': result.test.dimension,
                'summary': ', '.join(eval_summary[:3]),
            },
        )
        return redirect('community_feed')
    return render(request, 'psychometrics/share_result.html', {'result': result})


MAPA_SLUGS = [
    'big-five-inventario-de-personalidad',
    'heridas-de-la-infancia-lise-bourbeau',
    'dirty-dozen-triada-oscura',
]

_MAPA_META = [
    {'slug': 'big-five-inventario-de-personalidad', 'n': '01', 'label': 'Personalidad', 'desc': 'Los 5 rasgos base que estructuran tu forma de ser'},
    {'slug': 'heridas-de-la-infancia-lise-bourbeau', 'n': '02', 'label': 'Origen', 'desc': 'De dónde vienen tus patrones más arraigados'},
    {'slug': 'dirty-dozen-triada-oscura', 'n': '03', 'label': 'Sombra', 'desc': 'Lo que operas de forma automática sin verlo'},
]


@login_required
def mapa_patrones(request):
    completed = {}
    for slug in MAPA_SLUGS:
        r = TestResult.objects.filter(
            user=request.user, test__slug=slug
        ).order_by('-completed_at').first()
        if r:
            completed[slug] = r

    tests_info = [{**m, 'result': completed.get(m['slug']), 'done': m['slug'] in completed}
                  for m in _MAPA_META]
    all_done = len(completed) == len(MAPA_SLUGS)
    next_slug = next((m['slug'] for m in _MAPA_META if m['slug'] not in completed), None)

    return render(request, 'psychometrics/mapa_patrones.html', {
        'tests_info': tests_info,
        'all_done': all_done,
        'next_slug': next_slug,
        'done_count': len(completed),
    })


@login_required
def mapa_patrones_resultado(request):
    from accounts.plan_utils import plan_at_least

    results = []
    for slug in MAPA_SLUGS:
        r = TestResult.objects.filter(
            user=request.user, test__slug=slug
        ).order_by('-completed_at').first()
        if r:
            results.append(r)

    if len(results) < len(MAPA_SLUGS):
        return redirect('mapa_patrones')

    cache_key = f"mapa_insight_{request.user.pk}_{'-'.join(str(r.pk) for r in results)}"
    insight = cache.get(cache_key)

    if not insight and request.GET.get('generar'):
        insight = _generate_mapa_insight(results)
        if insight:
            cache.set(cache_key, insight, 60 * 60 * 24)

    is_paid = plan_at_least(request.user, 'navegante')

    return render(request, 'psychometrics/mapa_patrones_resultado.html', {
        'results': {r.test.slug: r for r in results},
        'insight': insight,
        'is_paid': is_paid,
    })


def _generate_mapa_insight(results):
    import json as json_lib, re as re_lib
    from config.ai_client import call_ai

    tests_summary = [{'test': r.test.name, 'evaluacion': r.evaluation} for r in results]

    prompt = (
        'A partir de estos 3 resultados de tests psicométricos de la misma persona, '
        'identificá 3 patrones que emergen en conjunto. '
        'Respondé SOLO con JSON válido, sin texto extra. Formato exacto:\n'
        '{"patron1":{"titulo":"...","descripcion":"...(2-3 oraciones)"},'
        '"patron2":{"titulo":"...","descripcion":"..."},'
        '"patron3":{"titulo":"...","descripcion":"..."},'
        '"reflejo_integrador":"...(1 párrafo breve que conecta los 3)"}\n\n'
        f'Resultados: {json_lib.dumps(tests_summary, ensure_ascii=False)}\n\n'
        'Son observaciones para la reflexión, no diagnósticos. Tutear. Tono directo, no condescendiente.'
    )

    raw = call_ai([{'role': 'user', 'content': prompt}], max_tokens=700, timeout=30)
    if not raw:
        return None

    match = re_lib.search(r'\{.*\}', raw, re_lib.DOTALL)
    if not match:
        return None

    try:
        return json_lib.loads(match.group())
    except Exception:
        return None


@login_required
def my_results(request):
    results = TestResult.objects.filter(user=request.user).select_related('test').order_by('-completed_at')
    return render(request, 'psychometrics/my_results.html', {'results': results})


@login_required
def mapa_interior(request):
    results = TestResult.objects.filter(user=request.user).select_related('test').order_by('-completed_at')
    # Build radar data: latest result per dimension
    dimension_data = {}
    for r in results:
        dim = r.test.dimension
        if dim not in dimension_data:
            total = 0
            count = 0
            for k, v in r.evaluation.items():
                if isinstance(v, (int, float)):
                    total += v
                    count += 1
            normalized = round((total / count) * 10) if count else 0
            dimension_data[dim] = {
                'label': r.test.get_dimension_display(),
                'value': min(100, normalized),
                'color': DIMENSION_COLORS.get(dim, '#7ECCCD'),
                'test_name': r.test.name,
                'date': r.completed_at.strftime('%d %b %Y'),
                'result_pk': r.pk,
            }

    radar_json = json.dumps(list(dimension_data.values()))
    return render(request, 'psychometrics/mapa_interior.html', {
        'dimension_data': dimension_data,
        'radar_json': radar_json,
        'results': results[:10],
    })


@login_required
def reponer_resultados(request):
    if request.method == 'POST':
        test_ids = request.POST.getlist('tests')
        deleted = TestResult.objects.filter(user=request.user, test__id__in=test_ids).delete()
        count = deleted[0]
        from django.contrib import messages
        messages.success(request, f'{count} resultado(s) eliminados. Puedes volver a tomar los tests.')
        return redirect('my_results')
    tests_con_resultado = Test.objects.filter(
        testresult__user=request.user, active=True
    ).distinct()
    return render(request, 'psychometrics/reponer_resultados.html', {'tests': tests_con_resultado})


def _generate_insight(result):
    from config.ai_client import call_ai
    return call_ai([{
        'role': 'user',
        'content': (
            f'Dame un insight breve (3-4 oraciones) sobre este resultado de test psicométrico. '
            f'Test: {result.test.name}. Dimensión: {result.test.dimension}. '
            f'Evaluación: {json.dumps(result.evaluation, ensure_ascii=False)}. '
            f'Recuerda: los resultados NO son deterministas, son puntos de exploración.'
        )
    }], max_tokens=300, timeout=20)
