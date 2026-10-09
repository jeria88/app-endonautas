"""Horarios de la consultoría: bloques de CONSULTORIA_MIN dentro de la disponibilidad semanal,
desde ahora + anticipación hasta el horizonte, menos los ocupados (pagados, o con pago pendiente
reciente que todavía los aparta)."""
from datetime import datetime, timedelta

from django.utils import timezone

from .constants import (CONSULTORIA_ANTICIPACION_H, CONSULTORIA_HORIZONTE_DIAS, CONSULTORIA_MIN,
                        CONSULTORIA_RETENCION_MIN)
from .models import ConsultoriaReserva, DisponibilidadConsultoria


def bloques(franjas, desde: datetime, hasta: datetime, minutos: int = CONSULTORIA_MIN) -> list[datetime]:
    """Inicios posibles (pura). `franjas`: [(dia_semana, hora_inicio, hora_fin)] en hora local."""
    tz = timezone.get_current_timezone()
    salida, dia = [], desde.astimezone(tz).date()
    while dia <= hasta.astimezone(tz).date():
        for d, ini, fin in franjas:
            if d != dia.weekday():
                continue
            t = timezone.make_aware(datetime.combine(dia, ini), tz)
            limite = timezone.make_aware(datetime.combine(dia, fin), tz)
            while t + timedelta(minutes=minutos) <= limite:
                if desde <= t <= hasta:
                    salida.append(t)
                t += timedelta(minutes=minutos)
        dia += timedelta(days=1)
    return sorted(salida)


def ocupados() -> set[datetime]:
    corte = timezone.now() - timedelta(minutes=CONSULTORIA_RETENCION_MIN)
    qs = ConsultoriaReserva.objects.filter(status=ConsultoriaReserva.STATUS_PAID) | \
        ConsultoriaReserva.objects.filter(status=ConsultoriaReserva.STATUS_PENDING, created_at__gte=corte)
    return set(qs.values_list('inicio', flat=True))


def disponibles(ahora: datetime = None) -> list[datetime]:
    ahora = ahora or timezone.now()
    franjas = list(DisponibilidadConsultoria.objects.filter(activo=True)
                   .values_list('dia_semana', 'hora_inicio', 'hora_fin'))
    desde = ahora + timedelta(hours=CONSULTORIA_ANTICIPACION_H)
    hasta = ahora + timedelta(days=CONSULTORIA_HORIZONTE_DIAS)
    tomados = ocupados()
    return [b for b in bloques(franjas, desde, hasta) if b not in tomados]
