"""
Calcula KPIs desde Django ORM para una semana dada.
"""
from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def calculate_week(week_start):
    """
    week_start: date object (lunes de la semana).
    Devuelve dict con todos los KPIs calculables desde ORM.
    """
    week_end = week_start + timedelta(days=7)
    # date → datetime aware para campos DateTimeField
    dt_start = timezone.make_aware(datetime.combine(week_start, datetime.min.time()))
    dt_end = timezone.make_aware(datetime.combine(week_end, datetime.min.time()))

    registros_nuevos = User.objects.filter(
        date_joined__gte=dt_start,
        date_joined__lt=dt_end,
    ).count()

    # Activación: usuarios de la semana que hicieron ≥1 test en sus primeros 7 días
    activacion_pct = _calc_activacion(week_start, week_end)

    # Retención: usuarios activos en Espejo en el período d7 / d30
    retencion_d7_pct = _calc_retencion(days=7)
    retencion_d30_pct = _calc_retencion(days=30)

    # Sesiones Espejo promedio por usuario activo (últimos 30 días)
    sesiones_espejo_avg = _calc_sesiones_espejo_avg()

    # Navegantes
    navegantes_total = _count_plan('navegante')
    navegantes_nuevos_semana = _count_plan_nuevos(week_start, week_end)

    # MRR estimado: navegante $10/mes, practicante $39/mes
    mrr_estimado_usd = _calc_mrr()

    return {
        'registros_nuevos': registros_nuevos,
        'activacion_pct': activacion_pct,
        'retencion_d7_pct': retencion_d7_pct,
        'retencion_d30_pct': retencion_d30_pct,
        'sesiones_espejo_avg': sesiones_espejo_avg,
        'navegantes_total': navegantes_total,
        'navegantes_nuevos_semana': navegantes_nuevos_semana,
        'mrr_estimado_usd': mrr_estimado_usd,
    }


def _calc_activacion(week_start, week_end):
    try:
        from psychometrics.models import TestResult
        dt_start = timezone.make_aware(datetime.combine(week_start, datetime.min.time()))
        dt_end = timezone.make_aware(datetime.combine(week_end, datetime.min.time()))
        nuevos_ids = User.objects.filter(
            date_joined__gte=dt_start,
            date_joined__lt=dt_end,
        ).values_list('id', flat=True)
        if not nuevos_ids:
            return 0.0
        activados = 0
        for uid in nuevos_ids:
            user = User.objects.get(pk=uid)
            cutoff = user.date_joined + timedelta(days=7)
            if TestResult.objects.filter(user=user, created_at__lte=cutoff).exists():
                activados += 1
        return round(activados / len(nuevos_ids) * 100, 1)
    except Exception:
        return 0.0


def _calc_retencion(days):
    try:
        from mirror.models import ChatSession
        cutoff = timezone.now() - timedelta(days=days)
        total = User.objects.filter(date_joined__lte=cutoff).count()
        if not total:
            return 0.0
        activos = User.objects.filter(
            date_joined__lte=cutoff,
            mirror_sessions__updated_at__gte=cutoff,
        ).distinct().count()
        return round(activos / total * 100, 1)
    except Exception:
        return 0.0


def _calc_sesiones_espejo_avg():
    try:
        from mirror.models import ChatSession
        from django.db.models import Count
        cutoff = timezone.now() - timedelta(days=30)
        qs = ChatSession.objects.filter(updated_at__gte=cutoff).values('user').annotate(
            n=Count('id')
        )
        if not qs:
            return 0.0
        return round(sum(r['n'] for r in qs) / len(qs), 2)
    except Exception:
        return 0.0


def _count_plan(plan_name):
    try:
        from accounts.models import UserProfile
        return UserProfile.objects.filter(plan=plan_name).count()
    except Exception:
        return 0


def _count_plan_nuevos(week_start, week_end):
    try:
        from accounts.models import UserProfile
        dt_start = timezone.make_aware(datetime.combine(week_start, datetime.min.time()))
        dt_end = timezone.make_aware(datetime.combine(week_end, datetime.min.time()))
        # ponytail: aproximación por date_joined del user, no fecha de upgrade
        return UserProfile.objects.filter(
            plan__in=['navegante', 'practicante', 'empresa'],
            user__date_joined__gte=dt_start,
            user__date_joined__lt=dt_end,
        ).count()
    except Exception:
        return 0


def _calc_mrr():
    try:
        from accounts.models import UserProfile
        nav = UserProfile.objects.filter(plan='navegante').count()
        prac = UserProfile.objects.filter(plan='practicante').count()
        emp = UserProfile.objects.filter(plan='empresa').count()
        return round(nav * 10 + prac * 39 + emp * 99, 2)
    except Exception:
        return 0.0
