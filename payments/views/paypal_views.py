import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..constants import PACKS
from ..models import FractonesPack, Subscription
from ..services import paypal as paypal_service
from tokens import service as token_service

logger = logging.getLogger(__name__)

_PLAN_SLUGS = frozenset(['navegante', 'practicante'])
_PACK_SLUGS = frozenset(PACKS.keys())


@login_required
def suscribir(request, plan):
    if plan not in _PLAN_SLUGS:
        return redirect('tokens_balance')

    return_url = request.build_absolute_uri(reverse('pago_paypal_retorno')) + f'?plan={plan}'
    cancel_url = request.build_absolute_uri(reverse('tokens_balance'))

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


@login_required
def pack(request, slug):
    if slug not in _PACK_SLUGS:
        return redirect('tokens_balance')

    return_url = request.build_absolute_uri(reverse('pago_paypal_pack_retorno')) + f'?slug={slug}'
    cancel_url = request.build_absolute_uri(reverse('tokens_balance'))

    try:
        order_id, approve_url = paypal_service.create_order(
            pack_slug=slug,
            return_url=return_url,
            cancel_url=cancel_url,
        )
    except Exception as e:
        logger.error(f'PayPal create_order error: {e}')
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'No se pudo conectar con PayPal. Intenta de nuevo.',
        })

    pack_info = PACKS[slug]
    FractonesPack.objects.create(
        user=request.user, gateway='paypal', pack_slug=slug,
        fractones=pack_info['fractones'],
        amount_local=pack_info['price_usd'],
        currency='USD',
        gateway_payment_id=order_id,
        status='pending',
    )
    return redirect(approve_url)


@login_required
def retorno_pack(request):
    order_id = request.GET.get('token')
    slug = request.GET.get('slug', '')

    if not order_id:
        return render(request, 'payments/resultado.html', {'exito': False})

    try:
        capture = paypal_service.capture_order(order_id)
        if capture.get('status') == 'COMPLETED':
            fp = FractonesPack.objects.filter(
                user=request.user, gateway='paypal',
                gateway_payment_id=order_id, status='pending',
            ).first()
            if fp:
                fp.status = 'paid'
                fp.save(update_fields=['status', 'updated_at'])
                token_service.credit_permanent(request.user, fp.fractones, reason=f'pack:{fp.pack_slug}')
                return render(request, 'payments/resultado.html', {
                    'exito': True, 'es_pack': True,
                    'fractones': fp.fractones, 'gateway': 'PayPal',
                    'mensaje': f'+{fp.fractones} fractones permanentes acreditados.',
                })
    except Exception as e:
        logger.error(f'PayPal retorno_pack error: {e}')

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
