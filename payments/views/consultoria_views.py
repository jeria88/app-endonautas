"""Consultoría 1:1 de 60 min ($29.990, MercadoPago) con agenda propia — patrón del checkout del ebook.

Flujo: /consultoria/ muestra los horarios libres (payments/consultoria.py) → el visitante elige,
deja nombre/email/motivo → reserva 'pending' que aparta el horario 30 min → MercadoPago →
retorno del navegador **o** webhook (red de seguridad) → _marcar_pagada: confirma al cliente por
email y avisa al harness (venta + consultoria_agendada → el dueño recibe el aviso por Telegram).
"""
import logging
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from ..consultoria import disponibles
from ..constants import CONSULTORIA_MIN, CONSULTORIA_SLUG, PRODUCTS
from ..models import ConsultoriaReserva
from ..services import harness
from ..services import mp as mp_service
from .taller_views import _get_or_create_user

logger = logging.getLogger(__name__)


def _fmt(dt) -> str:
    local = timezone.localtime(dt)
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    return f'{dias[local.weekday()]} {local:%d-%m-%Y} a las {local:%H:%M}'


def pagina(request):
    slots = disponibles()
    por_dia = {}
    for s in slots:
        local = timezone.localtime(s)
        por_dia.setdefault(local.date(), []).append({'iso': s.isoformat(), 'hora': f'{local:%H:%M}'})
    errores = {'horario': 'Ese horario ya no está disponible. Elige otro.',
               'datos': 'Revisa tu nombre y tu email.',
               'mp': 'No se pudo conectar con MercadoPago. Intenta de nuevo.'}
    return render(request, 'payments/consultoria.html', {
        'por_dia': [{'fecha': _fmt(timezone.make_aware(datetime.combine(d, datetime.min.time()))).rsplit(' a las', 1)[0],
                     'slots': v} for d, v in sorted(por_dia.items())],
        'precio': f"${PRODUCTS[CONSULTORIA_SLUG]['price_clp']:,}".replace(',', '.'),
        'minutos': CONSULTORIA_MIN,
        'error': errores.get(request.GET.get('err', '')),
    })


@require_POST
def reservar(request):
    email = (request.POST.get('email') or '').strip().lower()
    nombre = (request.POST.get('nombre') or '').strip()[:80]
    motivo = (request.POST.get('motivo') or '').strip()[:1000]
    canal_origen = (request.POST.get('canal_origen') or '').strip()[:40]
    base = reverse('consultoria')
    if not email or '@' not in email or not nombre:
        return redirect(f'{base}?err=datos')
    try:
        inicio = datetime.fromisoformat(request.POST.get('inicio', ''))
    except ValueError:
        return redirect(f'{base}?err=horario')
    if inicio not in set(disponibles()):
        return redirect(f'{base}?err=horario')

    user = _get_or_create_user(request, email, first_name=nombre, send_setup=False)
    ConsultoriaReserva.objects.filter(user=user, status=ConsultoriaReserva.STATUS_PENDING).delete()
    reserva = ConsultoriaReserva.objects.create(
        user=user, inicio=inicio, duracion_min=CONSULTORIA_MIN,
        amount_local=PRODUCTS[CONSULTORIA_SLUG]['price_clp'], motivo=motivo, canal_origen=canal_origen,
    )
    harness.emitir('checkout_iniciado', {'email': email, 'nombre': nombre, 'fuente': 'consultoria'},
                   datos={'producto': CONSULTORIA_SLUG, 'pasarela': 'mp', 'inicio': inicio.isoformat()},
                   dedupe_key=f'consultoria-{reserva.pk}-checkout')
    retorno = request.build_absolute_uri(reverse('consultoria_retorno_mp'))
    try:
        pref_id, init_point = mp_service.create_preference_product(
            CONSULTORIA_SLUG, user,
            success_url=f'{retorno}?rid={reserva.pk}&status=success',
            failure_url=f'{retorno}?rid={reserva.pk}&status=failure',
            pending_url=f'{retorno}?rid={reserva.pk}&status=pending',
            notification_url=request.build_absolute_uri(reverse('pago_mp_webhook')),
            extra_metadata={'reserva_id': str(reserva.pk)},
        )
    except Exception as e:
        logger.error(f'MP consultoria preference error: {e}')
        reserva.delete()
        return redirect(f'{base}?err=mp')
    reserva.gateway_payment_id = pref_id
    reserva.save(update_fields=['gateway_payment_id', 'updated_at'])
    return redirect(init_point)


def retorno_mp(request):
    payment_id = request.GET.get('payment_id') or request.GET.get('collection_id')
    status = request.GET.get('status') or request.GET.get('collection_status')
    rid = request.GET.get('rid', '')
    if status == 'pending':
        return render(request, 'payments/resultado.html', {
            'exito': True, 'pendiente': True,
            'mensaje': 'Tu pago está pendiente. Apenas se acredite te llega la confirmación por email.'})
    if status == 'success' and payment_id and rid.isdigit():
        try:
            if mp_service.get_payment(payment_id).get('status') == 'approved':
                reserva = ConsultoriaReserva.objects.filter(pk=rid).first()
                if reserva and reserva.status == ConsultoriaReserva.STATUS_PENDING:
                    _marcar_pagada(reserva, str(payment_id))
                if reserva and reserva.status == ConsultoriaReserva.STATUS_PAID:
                    return render(request, 'payments/resultado.html', {
                        'exito': True, 'mensaje': f'Consultoría agendada para el {_fmt(reserva.inicio)}. '
                                                  'Te llegó la confirmación por email.'})
                if reserva and reserva.status == ConsultoriaReserva.STATUS_CANCELLED:
                    return render(request, 'payments/resultado.html', {
                        'exito': False, 'mensaje': 'Ese horario se ocupó mientras pagabas. Te escribo hoy '
                                                   'para reagendar o devolverte el pago.'})
        except Exception as e:
            logger.error(f'MP retorno consultoria error: {e}')
    return render(request, 'payments/resultado.html', {
        'exito': False, 'mensaje': 'No se pudo confirmar el pago. Si ya fue cobrado, escríbenos a hola@endonautas.cl.'})


def _marcar_pagada(reserva, gateway_payment_id):
    """Idempotente: solo actúa sobre una reserva 'pending'. Si el horario ya tiene otra consultoría
    pagada (carrera entre dos pagos), esta queda cancelada y se le avisa al dueño para devolver."""
    try:
        with transaction.atomic():
            n = ConsultoriaReserva.objects.filter(pk=reserva.pk, status=ConsultoriaReserva.STATUS_PENDING).update(
                status=ConsultoriaReserva.STATUS_PAID, gateway_payment_id=gateway_payment_id)
    except IntegrityError:
        ConsultoriaReserva.objects.filter(pk=reserva.pk).update(status=ConsultoriaReserva.STATUS_CANCELLED)
        reserva.refresh_from_db()
        harness.emitir('escalado_al_dueño', {'email': reserva.user.email, 'fuente': 'consultoria'},
                       datos={'aviso': 'consultoria_choque_horario', 'inicio': reserva.inicio.isoformat(),
                              'pago': gateway_payment_id}, dedupe_key=f'consultoria-{reserva.pk}-choque')
        return False
    reserva.refresh_from_db()
    if not n:
        return False
    contacto = {'email': reserva.user.email, 'nombre': reserva.user.first_name or None, 'fuente': 'consultoria'}
    harness.emitir('venta', contacto, monto_clp=int(reserva.amount_local),
                   datos={'producto': CONSULTORIA_SLUG, 'pasarela': 'mp', 'external_ref': gateway_payment_id},
                   dedupe_key=f'consultoria-{reserva.pk}-venta',
                   atribucion=f'externo:{reserva.canal_origen or "directo"}')
    harness.emitir('consultoria_agendada', contacto,
                   datos={'inicio': reserva.inicio.isoformat(), 'cuando': _fmt(reserva.inicio),
                          'motivo': reserva.motivo[:300]},
                   dedupe_key=f'consultoria-{reserva.pk}-agendada')
    _confirmar(reserva)
    return True


def _confirmar(reserva):
    nombre = (reserva.user.first_name or '').strip()
    enlace = getattr(settings, 'CONSULTORIA_LINK', '') or ''
    cuerpo = (
        f'{"Hola " + nombre if nombre else "Hola"}.\n\n'
        f'Tu consultoría quedó agendada para el {_fmt(reserva.inicio)} (hora de Chile), '
        f'{reserva.duracion_min} minutos.\n\n'
        + (f'El enlace de la videollamada: {enlace}\n\n' if enlace else
           'Antes de la sesión te escribo con el enlace de la videollamada.\n\n')
        + 'Si necesitas cambiar el horario, responde este correo con al menos 24 horas de anticipación.\n\n'
        '— Franco'
    )
    try:
        send_mail('Tu consultoría está agendada', cuerpo, None, [reserva.user.email], fail_silently=False)
    except Exception as e:  # la reserva queda pagada igual; el dueño ya tiene el aviso por Telegram
        logger.error(f'consultoria confirmacion {reserva.pk}: {e}')
