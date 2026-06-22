import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..constants import PACKS
from ..models import FractonesPack, Subscription
from ..services import mp as mp_service
from tokens import service as token_service

logger = logging.getLogger(__name__)

_PLAN_SLUGS = frozenset(['navegante', 'practicante'])
_PACK_SLUGS = frozenset(PACKS.keys())


@login_required
def suscribir(request, plan):
    if plan not in _PLAN_SLUGS:
        return redirect('tokens_balance')

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


@login_required
def pack(request, slug):
    if slug not in _PACK_SLUGS:
        return redirect('tokens_balance')

    base_url = request.build_absolute_uri(reverse('pago_mp_pack_retorno'))

    try:
        preference_id, init_point = mp_service.create_preference(
            pack_slug=slug,
            user=request.user,
            success_url=f'{base_url}?slug={slug}&status=success',
            failure_url=f'{base_url}?slug={slug}&status=failure',
            pending_url=f'{base_url}?slug={slug}&status=pending',
        )
    except Exception as e:
        logger.error(f'MP create_preference error: {e}')
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'No se pudo conectar con MercadoPago. Intenta de nuevo.',
        })

    pack_info = PACKS[slug]
    FractonesPack.objects.create(
        user=request.user, gateway='mp', pack_slug=slug,
        fractones=pack_info['fractones'],
        amount_local=pack_info['price_clp'],
        currency='CLP',
        gateway_payment_id=preference_id,
        status='pending',
    )
    return redirect(init_point)


@login_required
def retorno_pack(request):
    payment_id = request.GET.get('payment_id') or request.GET.get('collection_id')
    status = request.GET.get('status') or request.GET.get('collection_status')
    slug = request.GET.get('slug', '')

    if status == 'pending':
        return render(request, 'payments/resultado.html', {
            'exito': True, 'pendiente': True,
            'mensaje': 'Tu pago está pendiente. Los fractones se acreditarán cuando se confirme.',
        })

    if status == 'failure':
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'El pago no fue procesado.',
        })

    if status == 'success' and payment_id:
        try:
            payment = mp_service.get_payment(payment_id)
            if payment.get('status') == 'approved':
                fp = FractonesPack.objects.filter(
                    user=request.user, gateway='mp', pack_slug=slug, status='pending',
                ).order_by('-created_at').first()
                if fp:
                    fp.status = 'paid'
                    fp.gateway_payment_id = str(payment_id)
                    fp.save(update_fields=['status', 'gateway_payment_id', 'updated_at'])
                    token_service.credit_permanent(request.user, fp.fractones, reason=f'pack:{slug}')
                    return render(request, 'payments/resultado.html', {
                        'exito': True, 'es_pack': True,
                        'fractones': fp.fractones, 'gateway': 'MercadoPago',
                        'mensaje': f'+{fp.fractones} fractones permanentes acreditados.',
                    })
        except Exception as e:
            logger.error(f'MP retorno_pack error: {e}')

    return render(request, 'payments/resultado.html', {
        'exito': False, 'mensaje': 'No se pudo confirmar el pago. Si ya fue cobrado, escríbenos.',
    })


@login_required
@require_POST
def api_preferencia_pack(request, slug):
    if slug not in _PACK_SLUGS:
        return JsonResponse({'error': 'Pack inválido'}, status=400)

    base_url = request.build_absolute_uri(reverse('pago_mp_pack_retorno'))

    try:
        preference_id, _ = mp_service.create_preference(
            pack_slug=slug,
            user=request.user,
            success_url=f'{base_url}?slug={slug}&status=success',
            failure_url=f'{base_url}?slug={slug}&status=failure',
            pending_url=f'{base_url}?slug={slug}&status=pending',
        )
    except Exception as e:
        logger.error(f'MP api_preferencia_pack error: {e}')
        return JsonResponse({'error': 'No se pudo crear la preferencia'}, status=500)

    pack_info = PACKS[slug]
    FractonesPack.objects.filter(user=request.user, gateway='mp', pack_slug=slug, status='pending').delete()
    FractonesPack.objects.create(
        user=request.user, gateway='mp', pack_slug=slug,
        fractones=pack_info['fractones'],
        amount_local=pack_info['price_clp'],
        currency='CLP',
        gateway_payment_id=preference_id,
        status='pending',
    )
    return JsonResponse({'preference_id': preference_id})


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
    pack_slug = metadata.get('pack_slug')
    user_id = metadata.get('user_id')

    if not pack_slug or not user_id:
        return

    fp = FractonesPack.objects.filter(
        user_id=user_id, gateway='mp', pack_slug=pack_slug, status='pending',
    ).order_by('-created_at').first()

    if fp:
        fp.status = 'paid'
        fp.gateway_payment_id = payment_id
        fp.save(update_fields=['status', 'gateway_payment_id', 'updated_at'])
        token_service.credit_permanent(fp.user, fp.fractones, reason=f'pack:{pack_slug}')
