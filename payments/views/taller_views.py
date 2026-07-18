import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..constants import TALLERES
from ..models import TallerReserva
from ..services import mp as mp_service

logger = logging.getLogger(__name__)

_TALLER_SLUGS = frozenset(TALLERES.keys())


def _get_or_create_user(request, email, first_name=''):
    """Cuenta automática para checkout de invitado. Si es nueva, dispara el flujo
    estándar de recuperación de contraseña para que el usuario la fije él mismo.

    NUNCA loguea la sesión como este user — si el email ya pertenece a una cuenta
    existente, eso sería iniciar sesión como otra persona sin verificar contraseña.
    """
    User = get_user_model()
    user, created = User.objects.get_or_create(
        email=email, defaults={'first_name': first_name},
    )
    if created:
        user.set_password(get_random_string(32))
        user.save(update_fields=['password'])
        form = PasswordResetForm({'email': email})
        if form.is_valid():
            form.save(
                request=request,
                token_generator=default_token_generator,
                email_template_name='accounts/email/password_reset.txt',
                subject_template_name='accounts/email/password_reset_subject.txt',
            )
    return user


@csrf_exempt
@require_POST
def reservar(request, slug):
    """Entrada pública (sin cuenta requerida) — landing externa envía email por POST.
    No crea sesión: la confirmación de retorno se correlaciona por el id de la
    reserva (rid), no por request.user — evita loguear al requester como el
    dueño real de un email preexistente."""
    if slug not in _TALLER_SLUGS:
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'Taller inválido.',
        })

    email = (request.POST.get('email') or '').strip().lower()
    if not email or '@' not in email:
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'Email inválido.',
        })

    user = _get_or_create_user(request, email, first_name=request.POST.get('first_name', ''))

    taller_info = TALLERES[slug]
    TallerReserva.objects.filter(user=user, gateway='mp', taller_slug=slug, status='pending').delete()
    reserva = TallerReserva.objects.create(
        user=user, gateway='mp', taller_slug=slug,
        amount_local=taller_info['price_clp'], currency='CLP',
        status='pending',
    )

    base_url = request.build_absolute_uri(reverse('pago_mp_taller_retorno'))

    try:
        preference_id, init_point = mp_service.create_preference_taller(
            taller_slug=slug,
            user=user,
            success_url=f'{base_url}?slug={slug}&rid={reserva.pk}&status=success',
            failure_url=f'{base_url}?slug={slug}&rid={reserva.pk}&status=failure',
            pending_url=f'{base_url}?slug={slug}&rid={reserva.pk}&status=pending',
        )
    except Exception as e:
        logger.error(f'MP create_preference_taller error: {e}')
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'No se pudo conectar con MercadoPago. Intenta de nuevo.',
        })

    reserva.gateway_payment_id = preference_id
    reserva.save(update_fields=['gateway_payment_id', 'updated_at'])
    return redirect(init_point)


def retorno(request):
    payment_id = request.GET.get('payment_id') or request.GET.get('collection_id')
    status = request.GET.get('status') or request.GET.get('collection_status')
    rid = request.GET.get('rid', '')

    if status == 'pending':
        return render(request, 'payments/resultado.html', {
            'exito': True, 'pendiente': True,
            'mensaje': 'Tu seña está pendiente de confirmación. Te avisamos por email apenas se acredite.',
        })

    if status == 'failure':
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'El pago no fue procesado.',
        })

    if status == 'success' and payment_id and rid:
        try:
            payment = mp_service.get_payment(payment_id)
            if payment.get('status') == 'approved':
                tr = TallerReserva.objects.filter(pk=rid, gateway='mp', status='pending').first()
                if tr:
                    tr.status = 'paid'
                    tr.gateway_payment_id = str(payment_id)
                    tr.save(update_fields=['status', 'gateway_payment_id', 'updated_at'])
                    return render(request, 'payments/resultado.html', {
                        'exito': True, 'gateway': 'MercadoPago',
                        'mensaje': 'Cupo reservado. Revisa tu email para definir tu contraseña y ver los detalles del taller.',
                    })
        except Exception as e:
            logger.error(f'MP retorno_taller error: {e}')

    return render(request, 'payments/resultado.html', {
        'exito': False, 'mensaje': 'No se pudo confirmar el pago. Si ya fue cobrado, escríbenos.',
    })
