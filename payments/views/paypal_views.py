import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..models import Subscription
from ..services import paypal as paypal_service
from accounts.listmonk import update_subscriber_lists
from tokens import service as token_service

logger = logging.getLogger(__name__)

_PLAN_SLUGS = frozenset(['navegante', 'practicante'])


@login_required
def suscribir(request, plan):
    if plan not in _PLAN_SLUGS:
        return redirect('planes')

    return_url = request.build_absolute_uri(reverse('pago_paypal_retorno')) + f'?plan={plan}'
    cancel_url = request.build_absolute_uri(reverse('planes'))

    try:
        sub_id, approve_url = paypal_service.create_subscription(
            plan_slug=plan,
            return_url=return_url,
            cancel_url=cancel_url,
            user_email=request.user.email,
        )
    except Exception as e:
        logger.error(f'PayPal create_subscription error: {e}')
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'No se pudo conectar con PayPal. Intenta de nuevo.',
        })

    Subscription.objects.filter(user=request.user, gateway='paypal', status='pending').delete()
    Subscription.objects.create(
        user=request.user, gateway='paypal', plan=plan,
        status='pending', gateway_subscription_id=sub_id,
    )
    return redirect(approve_url)


@login_required
def retorno_suscripcion(request):
    sub_id = request.GET.get('subscription_id')
    plan = request.GET.get('plan', '')

    if not sub_id:
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'Suscripción no confirmada.',
        })

    try:
        data = paypal_service.get_subscription(sub_id)
        if data.get('status') in ('ACTIVE', 'APPROVED'):
            sub, _ = Subscription.objects.get_or_create(
                user=request.user, gateway='paypal', gateway_subscription_id=sub_id,
                defaults={'plan': plan or 'navegante', 'status': 'pending'},
            )
            sub.status = 'active'
            sub.started_at = timezone.now()
            sub.save(update_fields=['status', 'started_at', 'updated_at'])

            profile = request.user.profile
            profile.plan = sub.plan
            profile.save(update_fields=['plan'])
            update_subscriber_lists(request.user.email, sub.plan)
            token_service.renew_monthly(request.user)
            token_service.process_referral_conversion(request.user)

            return render(request, 'payments/resultado.html', {
                'exito': True, 'es_suscripcion': True,
                'plan': sub.plan, 'gateway': 'PayPal',
                'mensaje': f'¡Bienvenido al plan {sub.plan.title()}!',
            })
    except Exception as e:
        logger.error(f'PayPal retorno_suscripcion error: {e}')

    return render(request, 'payments/resultado.html', {
        'exito': False, 'mensaje': 'No se pudo confirmar el pago. Si ya fue cobrado, escríbenos.',
    })


@csrf_exempt
@require_POST
def webhook(request):
    try:
        raw_body = json.loads(request.body)

        if not paypal_service.verify_webhook_signature(request.headers, raw_body):
            logger.warning('PayPal webhook: firma inválida')
            return HttpResponse(status=400)

        event_type = raw_body.get('event_type', '')
        resource = raw_body.get('resource', {})

        if event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
            _activated(resource)
        elif event_type in ('BILLING.SUBSCRIPTION.CANCELLED', 'BILLING.SUBSCRIPTION.SUSPENDED'):
            _cancelled(resource)
        elif event_type == 'BILLING.SUBSCRIPTION.RENEWED':
            _renewed(resource)

    except Exception as e:
        logger.error(f'PayPal webhook error: {e}')

    return HttpResponse(status=200)


def _activated(resource):
    sub_id = resource.get('id')
    sub = Subscription.objects.filter(gateway='paypal', gateway_subscription_id=sub_id).first()
    if sub and sub.status != 'active':
        sub.status = 'active'
        sub.started_at = timezone.now()
        sub.save(update_fields=['status', 'started_at', 'updated_at'])
        profile = sub.user.profile
        if profile.plan != sub.plan:
            profile.plan = sub.plan
            profile.save(update_fields=['plan'])
        update_subscriber_lists(sub.user.email, sub.plan)
        token_service.renew_monthly(sub.user)


def _cancelled(resource):
    sub_id = resource.get('id')
    sub = Subscription.objects.filter(gateway='paypal', gateway_subscription_id=sub_id).first()
    if sub and sub.status in ('active', 'pending'):
        sub.status = 'cancelled'
        sub.cancelled_at = timezone.now()
        sub.save(update_fields=['status', 'cancelled_at', 'updated_at'])
        profile = sub.user.profile
        profile.plan = 'free'
        profile.save(update_fields=['plan'])


def _renewed(resource):
    sub_id = resource.get('id')
    sub = Subscription.objects.filter(gateway='paypal', gateway_subscription_id=sub_id).first()
    if sub and sub.status == 'active':
        token_service.renew_monthly(sub.user)
