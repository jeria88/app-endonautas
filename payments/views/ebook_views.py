import logging

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from accounts.listmonk import LIST_LANZAMIENTO, subscribe_user

from ..constants import PRODUCTS
from ..models import EbookLead, EbookOrder
from ..services import mp as mp_service
from ..services import paypal as paypal_service
from .taller_views import _get_or_create_user

logger = logging.getLogger(__name__)

PRODUCT_SLUG = 'endonautica-ebook'


@csrf_exempt
@require_POST
def lead(request):
    """Captura post-test de heridas: pide email o WhatsApp a cambio del PDF de la herida."""
    email = (request.POST.get('email') or '').strip().lower()
    whatsapp = (request.POST.get('whatsapp') or '').strip()
    herida = (request.POST.get('herida') or '').strip()
    canal_origen = (request.POST.get('canal_origen') or 'test-heridas').strip()

    if not email and not whatsapp:
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'Necesitamos un email o WhatsApp para enviarte el mapa.',
        })

    lead_obj = EbookLead.objects.create(
        email=email, whatsapp=whatsapp, herida=herida,
        canal_origen=canal_origen, status=EbookLead.STATUS_NUEVO,
    )
    if email and herida:
        from .entrega import entregar_pdf_herida
        entregar_pdf_herida(lead_obj)

    # Sin esto el lead solo existe en el admin de Django: recibe el PDF y nada más.
    # Es el activo más caro del funnel, así que entra a la lista de email desde el
    # primer contacto. La herida viaja como atributo para poder segmentar después.
    if email:
        subscribe_user(
            email, list_ids=[LIST_LANZAMIENTO],
            attribs={'herida': herida, 'origen': canal_origen},
        )

    return render(request, 'payments/resultado.html', {
        'exito': True,
        'mensaje': 'Listo. Revisa tu email en los próximos minutos con el mapa completo de tu herida.',
    })


@csrf_exempt
@require_POST
def comprar(request, gateway):
    """Checkout de invitado del ebook (mismo patrón que taller_views.reservar). gateway: mp|paypal."""
    if gateway not in ('mp', 'paypal'):
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'Método de pago inválido.',
        })

    email = (request.POST.get('email') or '').strip().lower()
    if not email or '@' not in email:
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'Email inválido.',
        })

    canal_origen = (request.POST.get('canal_origen') or '').strip()
    user = _get_or_create_user(
        request, email, first_name=request.POST.get('first_name', ''), send_setup=False,
    )
    product = PRODUCTS[PRODUCT_SLUG]

    # Quien llega al checkout y no termina de pagar es el lead más calificado que
    # hay, y hasta ahora solo dejaba una EbookOrder 'pending' que nadie mira.
    # `_marcar_pagado` lo pasa a 'comprado' al confirmarse, así que si vuelve y
    # paga, el estado se corrige solo.
    if not EbookLead.objects.filter(email=email).exists():
        EbookLead.objects.create(
            email=email, canal_origen=canal_origen or 'checkout',
            status=EbookLead.STATUS_CONTACTADO,
        )
    subscribe_user(email, list_ids=[LIST_LANZAMIENTO],
                   attribs={'origen': canal_origen or 'checkout'})

    EbookOrder.objects.filter(user=user, gateway=gateway, status=EbookOrder.STATUS_PENDING).delete()

    if gateway == 'mp':
        order = EbookOrder.objects.create(
            user=user, gateway='mp', amount_local=product['price_clp'], currency='CLP',
            status=EbookOrder.STATUS_PENDING, canal_origen=canal_origen,
        )
        base_url = request.build_absolute_uri(reverse('pago_ebook_retorno_mp'))
        try:
            preference_id, init_point = mp_service.create_preference_product(
                PRODUCT_SLUG, user,
                success_url=f'{base_url}?oid={order.pk}&status=success',
                failure_url=f'{base_url}?oid={order.pk}&status=failure',
                pending_url=f'{base_url}?oid={order.pk}&status=pending',
                notification_url=request.build_absolute_uri(reverse('pago_mp_webhook')),
            )
        except Exception as e:
            logger.error(f'MP create_preference_product error: {e}')
            return render(request, 'payments/resultado.html', {
                'exito': False, 'mensaje': 'No se pudo conectar con MercadoPago. Intenta de nuevo.',
            })
        order.gateway_payment_id = preference_id
        order.save(update_fields=['gateway_payment_id', 'updated_at'])
        return redirect(init_point)

    # paypal
    order = EbookOrder.objects.create(
        user=user, gateway='paypal', amount_local=product['price_usd'], currency='USD',
        status=EbookOrder.STATUS_PENDING, canal_origen=canal_origen,
    )
    base_url = request.build_absolute_uri(reverse('pago_ebook_retorno_paypal'))
    try:
        paypal_order_id, approve_url = paypal_service.create_order(
            PRODUCT_SLUG,
            return_url=f'{base_url}?oid={order.pk}',
            cancel_url=f'{base_url}?oid={order.pk}&status=cancel',
        )
    except Exception as e:
        logger.error(f'PayPal create_order error: {e}')
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'No se pudo conectar con PayPal. Intenta de nuevo.',
        })
    order.gateway_payment_id = paypal_order_id
    order.save(update_fields=['gateway_payment_id', 'updated_at'])
    return redirect(approve_url)


def _download_url(order, request, formato='pdf'):
    """El token ya existe cuando se confirma el pago, así que la pantalla de éxito
    puede entregar el libro sin esperar al correo. Si el email se demora, cae en
    promociones o rebota, el comprador igual se va con el archivo."""
    if not order.download_token:
        return ''
    path = reverse('descargar_ebook_formato', args=[order.download_token, formato])
    return request.build_absolute_uri(path)


def retorno_mp(request):
    payment_id = request.GET.get('payment_id') or request.GET.get('collection_id')
    status = request.GET.get('status') or request.GET.get('collection_status')
    oid = request.GET.get('oid', '')

    if status == 'pending':
        return render(request, 'payments/resultado.html', {
            'exito': True, 'pendiente': True,
            'mensaje': 'Tu pago está pendiente de confirmación. Te avisamos por email apenas se acredite.',
        })

    if status == 'failure':
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'El pago no fue procesado.',
        })

    if status == 'success' and payment_id and oid:
        try:
            payment = mp_service.get_payment(payment_id)
            if payment.get('status') == 'approved':
                order = EbookOrder.objects.filter(
                    pk=oid, gateway='mp', status=EbookOrder.STATUS_PENDING,
                ).first()
                if order:
                    _marcar_pagado(order, str(payment_id), request)
                    return render(request, 'payments/resultado.html', {
                        'exito': True, 'gateway': 'MercadoPago',
                        'mensaje': 'Pago confirmado. Aquí está tu libro.',
                        'download_url': _download_url(order, request, 'pdf'),
                'download_url_epub': _download_url(order, request, 'epub'),
                    })
        except Exception as e:
            logger.error(f'MP retorno_ebook error: {e}')

    return render(request, 'payments/resultado.html', {
        'exito': False, 'mensaje': 'No se pudo confirmar el pago. Si ya fue cobrado, escríbenos.',
    })


def retorno_paypal(request):
    oid = request.GET.get('oid', '')
    status = request.GET.get('status', '')

    if status == 'cancel':
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'Pago cancelado.',
        })

    order = EbookOrder.objects.filter(pk=oid, gateway='paypal', status=EbookOrder.STATUS_PENDING).first()
    if not order:
        return render(request, 'payments/resultado.html', {
            'exito': False, 'mensaje': 'No se pudo confirmar el pago. Si ya fue cobrado, escríbenos.',
        })

    try:
        result = paypal_service.capture_order(order.gateway_payment_id)
        if result.get('status') == 'COMPLETED':
            _marcar_pagado(order, order.gateway_payment_id, request)
            return render(request, 'payments/resultado.html', {
                'exito': True, 'gateway': 'PayPal',
                'mensaje': 'Pago confirmado. Aquí está tu libro.',
                'download_url': _download_url(order, request, 'pdf'),
                'download_url_epub': _download_url(order, request, 'epub'),
            })
    except Exception as e:
        logger.error(f'PayPal retorno_ebook error: {e}')

    return render(request, 'payments/resultado.html', {
        'exito': False, 'mensaje': 'No se pudo confirmar el pago. Si ya fue cobrado, escríbenos.',
    })


def _marcar_pagado(order, gateway_payment_id, request=None):
    order.status = EbookOrder.STATUS_PAID
    order.gateway_payment_id = gateway_payment_id
    order.download_token = get_random_string(48)
    order.save(update_fields=['status', 'gateway_payment_id', 'download_token', 'updated_at'])
    EbookLead.objects.filter(email=order.user.email).exclude(
        status=EbookLead.STATUS_COMPRADO,
    ).update(status=EbookLead.STATUS_COMPRADO)
    from .entrega import entregar_ebook
    entregar_ebook(order, request)
