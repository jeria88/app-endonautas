import json
import os

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from reports.models import KPISnapshot


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
