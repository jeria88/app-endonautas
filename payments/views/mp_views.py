import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..models import FractonesPack, Subscription, TallerReserva
from ..services import mp as mp_service
from accounts.listmonk import update_subscriber_lists
from tokens import service as token_service

logger = logging.getLogger(__name__)

_PLAN_SLUGS = frozenset(['navegante', 'practicante'])


@login_required
def suscribir(request, plan):
    if plan not in _PLAN_SLUGS:
        return redirect('planes')

    return_url = request.build_absolute_uri(reverse('pago_mp_retorno_suscripcion')) + f'?plan={plan}'

    try:
        preapproval_id, init_point = mp_service.create_preapproval(
            plan_slug=plan, user=request.user, return_url=return_url,
        )
    except Exception as e:
        logger.error(f'MP create_preapproval error: {e}')
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'No se pudo conectar con MercadoPago. Intenta de nuevo.',
        })

    Subscription.objects.filter(user=request.user, gateway='mp', status='pending').delete()
    Subscription.objects.create(
        user=request.user, gateway='mp', plan=plan,
        status='pending', gateway_subscription_id=preapproval_id,
    )
    return redirect(init_point)


@login_required
def retorno_suscripcion(request):
    preapproval_id = request.GET.get('preapproval_id')
    plan = request.GET.get('plan', '')

    if not preapproval_id:
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'Suscripción no confirmada.',
        })

    try:
        data = mp_service.get_preapproval(preapproval_id)
        mp_status = data.get('status')

        sub = Subscription.objects.filter(
            gateway='mp', gateway_subscription_id=preapproval_id
        ).first()

        if mp_status == 'authorized':
            if sub:
                sub.status = 'active'
                sub.started_at = timezone.now()
                sub.save(update_fields=['status', 'started_at', 'updated_at'])
                plan = sub.plan

            profile = request.user.profile
            profile.plan = plan
            profile.save(update_fields=['plan'])
            update_subscriber_lists(request.user.email, plan)
            token_service.renew_monthly(request.user)
            token_service.process_referral_conversion(request.user)

            return render(request, 'payments/resultado.html', {
                'exito': True, 'es_suscripcion': True,
                'plan': plan, 'gateway': 'MercadoPago',
                'mensaje': f'¡Bienvenido al plan {plan.title()}!',
            })

        elif mp_status == 'pending':
            return render(request, 'payments/resultado.html', {
                'exito': True, 'pendiente': True,
                'mensaje': 'Tu suscripción está pendiente de confirmación. Te avisaremos por email.',
            })

    except Exception as e:
        logger.error(f'MP retorno_suscripcion error: {e}')

    return render(request, 'payments/resultado.html', {
        'exito': False, 'mensaje': 'No se pudo confirmar el pago. Si ya fue cobrado, escríbenos.',
    })


@csrf_exempt
@require_POST
def webhook(request):
    try:
        x_signature = request.headers.get('x-signature', '')
        x_request_id = request.headers.get('x-request-id', '')
        body = json.loads(request.body)

        if not mp_service.verify_webhook(body, x_signature, x_request_id):
            logger.warning('MP webhook: firma inválida')
            return HttpResponse(status=400)

        topic = body.get('type') or request.GET.get('topic', '')
        data_id = body.get('data', {}).get('id')

        if not data_id:
            return HttpResponse(status=200)

        if topic == 'subscription_preapproval':
            _handle_preapproval(str(data_id))
        elif topic == 'subscription_authorized_payment':
            _handle_authorized_payment(str(data_id))
        elif topic == 'payment':
            _handle_one_time_payment(str(data_id))

    except Exception as e:
        logger.error(f'MP webhook error: {e}')

    return HttpResponse(status=200)


def _handle_preapproval(preapproval_id):
    data = mp_service.get_preapproval(preapproval_id)
    sub = Subscription.objects.filter(gateway='mp', gateway_subscription_id=preapproval_id).first()
    if not sub:
        return

    mp_status = data.get('status')
    if mp_status == 'authorized' and sub.status != 'active':
        sub.status = 'active'
        sub.started_at = timezone.now()
        sub.save(update_fields=['status', 'started_at', 'updated_at'])
        profile = sub.user.profile
        profile.plan = sub.plan
        profile.save(update_fields=['plan'])
        update_subscriber_lists(sub.user.email, sub.plan)
        token_service.renew_monthly(sub.user)
    elif mp_status == 'paused' and sub.status == 'active':
        sub.status = 'paused'
        sub.save(update_fields=['status', 'updated_at'])
    elif mp_status == 'cancelled':
        sub.status = 'cancelled'
        sub.cancelled_at = timezone.now()
        sub.save(update_fields=['status', 'cancelled_at', 'updated_at'])
        profile = sub.user.profile
        profile.plan = 'free'
        profile.save(update_fields=['plan'])


def _handle_authorized_payment(payment_id):
    payment = mp_service.get_payment(payment_id)
    if payment.get('status') != 'approved':
        return
    preapproval_id = payment.get('preapproval_id')
    if preapproval_id:
        sub = Subscription.objects.filter(gateway='mp', gateway_subscription_id=str(preapproval_id)).first()
        if sub and sub.status == 'active':
            token_service.renew_monthly(sub.user)


def _handle_one_time_payment(payment_id):
    payment = mp_service.get_payment(payment_id)
    if payment.get('status') != 'approved':
        return

    metadata = payment.get('metadata', {})
    user_id = metadata.get('user_id')
    if not user_id:
        return

    pack_slug = metadata.get('pack_slug')
    taller_slug = metadata.get('taller_slug')
    product_slug = metadata.get('product_slug')

    if product_slug == 'endonautica-ebook':
        # Red de seguridad del checkout del ebook: el retorno del navegador ya llama a
        # _marcar_pagado, pero si el comprador cierra la pestaña tras pagar, esta es la
        # única vía que entrega el libro. Idempotente: el filtro por status=PENDING hace
        # que la segunda llamada (retorno o reintento de MP) no encuentre nada.
        from ..models import EbookOrder
        from .ebook_views import _marcar_pagado
        order = EbookOrder.objects.filter(
            user_id=user_id, gateway='mp', status=EbookOrder.STATUS_PENDING,
        ).order_by('-created_at').first()
        if order:
            _marcar_pagado(order, str(payment_id))
        return

    if pack_slug:
        fp = FractonesPack.objects.filter(
            user_id=user_id, gateway='mp', pack_slug=pack_slug, status='pending',
        ).order_by('-created_at').first()
        if fp:
            fp.status = 'paid'
            fp.gateway_payment_id = payment_id
            fp.save(update_fields=['status', 'gateway_payment_id', 'updated_at'])
            token_service.credit_permanent(fp.user, fp.fractones, reason=f'pack:{pack_slug}')
    elif taller_slug:
        tr = TallerReserva.objects.filter(
            user_id=user_id, gateway='mp', taller_slug=taller_slug, status='pending',
        ).order_by('-created_at').first()
        if tr:
            tr.status = 'paid'
            tr.gateway_payment_id = payment_id
            tr.save(update_fields=['status', 'gateway_payment_id', 'updated_at'])
