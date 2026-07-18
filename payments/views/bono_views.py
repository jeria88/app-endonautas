import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from ..models import Subscription, TallerReserva
from ..services import mp as mp_service
from accounts.listmonk import update_subscriber_lists
from tokens import service as token_service

logger = logging.getLogger(__name__)

_TALLER_SLUG = 'taller1-terapeutas'
_BONO_PLAN = 'practicante'


def _enviar_reset(request, user):
    """Dispara un link de contraseña nuevo — el que se envió al pagar la seña
    (semanas antes) ya expiró (PASSWORD_RESET_TIMEOUT default de Django: 3 días)."""
    form = PasswordResetForm({'email': user.email})
    if form.is_valid():
        form.save(
            request=request,
            token_generator=default_token_generator,
            email_template_name='accounts/email/password_reset.txt',
            subject_template_name='accounts/email/password_reset_subject.txt',
        )


def activar(request):
    """QR genérico mostrado al final del taller presencial → esta página.
    Sin login: correlaciona por email contra una TallerReserva ya paga."""
    if request.method != 'POST':
        return render(request, 'payments/bono_taller.html', {})

    email = (request.POST.get('email') or '').strip().lower()
    User = get_user_model()
    user = User.objects.filter(email=email).first() if email else None

    if not user or not TallerReserva.objects.filter(
        user=user, taller_slug=_TALLER_SLUG, status='paid',
    ).exists():
        return render(request, 'payments/bono_taller.html', {
            'error': 'No encontramos un pago de seña confirmado con ese email. Si ya pagaste, escríbenos.',
        })

    if Subscription.objects.filter(user=user, plan=_BONO_PLAN).exclude(status='cancelled').exists():
        _enviar_reset(request, user)
        return render(request, 'payments/resultado.html', {
            'exito': True,
            'mensaje': 'Ya tenés el Plan Practicante activo. Revisa tu email para entrar a tu cuenta.',
        })

    return_url = request.build_absolute_uri(reverse('pago_mp_bono_taller_retorno'))

    try:
        preapproval_id, init_point = mp_service.create_preapproval(
            plan_slug=_BONO_PLAN, user=user, return_url=return_url, free_trial_months=1,
        )
    except Exception as e:
        logger.error(f'MP create_preapproval (bono taller) error: {e}')
        return render(request, 'payments/bono_taller.html', {
            'error': 'No se pudo conectar con MercadoPago. Intenta de nuevo.',
        })

    Subscription.objects.filter(user=user, gateway='mp', status='pending').delete()
    Subscription.objects.create(
        user=user, gateway='mp', plan=_BONO_PLAN,
        status='pending', gateway_subscription_id=preapproval_id,
    )
    return redirect(init_point)


def retorno(request):
    preapproval_id = request.GET.get('preapproval_id')

    if not preapproval_id:
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'Suscripción no confirmada.',
        })

    try:
        data = mp_service.get_preapproval(preapproval_id)
        mp_status = data.get('status')

        sub = Subscription.objects.filter(gateway='mp', gateway_subscription_id=preapproval_id).first()

        if mp_status == 'authorized':
            if sub and sub.status != 'active':
                sub.status = 'active'
                sub.started_at = timezone.now()
                sub.save(update_fields=['status', 'started_at', 'updated_at'])
                profile = sub.user.profile
                profile.plan = sub.plan
                profile.save(update_fields=['plan'])
                update_subscriber_lists(sub.user.email, sub.plan)
                token_service.renew_monthly(sub.user)
                _enviar_reset(request, sub.user)

            return render(request, 'payments/resultado.html', {
                'exito': True, 'es_suscripcion': True,
                'plan': _BONO_PLAN, 'gateway': 'MercadoPago',
                'mensaje': 'Mes gratis de Plan Practicante activado. Revisa tu email para definir tu contraseña y entrar.',
            })

        elif mp_status == 'pending':
            return render(request, 'payments/resultado.html', {
                'exito': True, 'pendiente': True,
                'mensaje': 'Tu autorización está pendiente de confirmación. Te avisamos por email.',
            })

    except Exception as e:
        logger.error(f'MP retorno bono_taller error: {e}')

    return render(request, 'payments/resultado.html', {
        'exito': False, 'mensaje': 'No se pudo confirmar la activación. Si ya autorizaste el pago, escríbenos.',
    })
