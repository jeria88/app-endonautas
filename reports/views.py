import json
import logging
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from reports.models import BugReport, BugScreenshot, KPISnapshot

logger = logging.getLogger(__name__)


def _auth_ok(request):
    expected = os.getenv('KPI_API_TOKEN', '')
    if not expected:
        return False
    auth = request.headers.get('Authorization', '')
    return auth == f'Bearer {expected}'


@require_GET
def weekly_latest(request):
    if not _auth_ok(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        weeks_back = int(request.GET.get('weeks_back', 1))
    except ValueError:
        weeks_back = 1

    snaps = KPISnapshot.objects.all()[:weeks_back]
    if not snaps:
        return JsonResponse({'error': 'No hay snapshots aún'}, status=404)

    def serialize(s):
        return {
            'week': f"{s.year}-W{s.week_number:02d}",
            'week_start': s.week_start.isoformat(),
            'escenario': s.escenario,
            'alertas': s.alertas,
            'decision_sugerida': s.decision_sugerida,
            'registros_nuevos': s.registros_nuevos,
            'activacion_pct': s.activacion_pct,
            'retencion_d7_pct': s.retencion_d7_pct,
            'retencion_d30_pct': s.retencion_d30_pct,
            'sesiones_espejo_avg': s.sesiones_espejo_avg,
            'navegantes_total': s.navegantes_total,
            'navegantes_nuevos_semana': s.navegantes_nuevos_semana,
            'mrr_estimado_usd': s.mrr_estimado_usd,
            'email_open_rate_pct': s.email_open_rate_pct,
            'email_ctr_pct': s.email_ctr_pct,
            'suscriptores_total': s.suscriptores_total,
            'visitas_landing': s.visitas_landing,
            'visitas_unicas': s.visitas_unicas,
            'fuentes_top': s.fuentes_top,
            'md_snapshot': s.md_snapshot,
            'created_at': s.created_at.isoformat(),
        }

    if weeks_back == 1:
        return JsonResponse(serialize(snaps[0]))

    return JsonResponse({'snapshots': [serialize(s) for s in snaps]})


@login_required
@require_POST
def bug_report(request):
    desc = (request.POST.get('descripcion') or '').strip()
    if not desc:
        return JsonResponse({'error': 'Describe el problema antes de enviar.'}, status=400)
    files = request.FILES.getlist('capturas')[:3]
    for f in files:
        if f.size > 3 * 1024 * 1024:
            return JsonResponse({'error': f'{f.name} supera 3MB.'}, status=400)
        if not (f.content_type or '').startswith('image/'):
            return JsonResponse({'error': f'{f.name} no es una imagen.'}, status=400)
    try:
        report = BugReport.objects.create(
            user=request.user,
            descripcion=desc,
            pagina=request.POST.get('pagina', '')[:300],
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:400],
        )
        for f in files:
            BugScreenshot.objects.create(
                report=report, imagen=f.read(), content_type=f.content_type or 'image/png')
    except Exception:
        logger.exception("bug_report: fallo al guardar")
        return JsonResponse({'error': 'No se pudo enviar el reporte. Intenta de nuevo.'}, status=500)
    return JsonResponse({'ok': True})


@staff_member_required
def bug_screenshot(request, pk):
    shot = BugScreenshot.objects.filter(pk=pk).first()
    if not shot:
        return HttpResponse(status=404)
    return HttpResponse(bytes(shot.imagen), content_type=shot.content_type)
