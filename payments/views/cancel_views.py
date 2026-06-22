import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from ..models import Subscription
from ..services import mp as mp_service
from ..services import paypal as paypal_service

logger = logging.getLogger(__name__)


@login_required
def cancelar_vista(request):
    """Show current subscription info and confirm cancellation."""
    sub = (
        Subscription.objects
        .filter(user=request.user, status='active')
        .order_by('-created_at')
        .first()
    )
    return render(request, 'payments/cancelar.html', {'sub': sub})


@login_required
@require_POST
def cancelar_confirmar(request):
    """Execute cancellation via gateway API, downgrade plan to free."""
    sub = (
        Subscription.objects
        .filter(user=request.user, status='active')
        .order_by('-created_at')
        .first()
    )

    if not sub:
        return render(request, 'payments/cancelar.html', {
            'sub': None, 'error': 'No tienes una suscripción activa.',
        })

    try:
        if sub.gateway == 'paypal':
            paypal_service.cancel_subscription(sub.gateway_subscription_id)
        elif sub.gateway == 'mp':
            mp_service.cancel_preapproval(sub.gateway_subscription_id)
    except Exception as e:
        logger.error(f'Cancel subscription error ({sub.gateway}): {e}')
        return render(request, 'payments/cancelar.html', {
            'sub': sub,
            'error': 'No pudimos cancelar con el procesador de pago. Escríbenos a hola@endonautas.cl.',
        })

    sub.status = 'cancelled'
    sub.cancelled_at = timezone.now()
    sub.save(update_fields=['status', 'cancelled_at', 'updated_at'])

    profile = request.user.profile
    profile.plan = 'free'
    profile.save(update_fields=['plan'])

    return render(request, 'payments/cancelar.html', {'sub': None, 'cancelado': True})
