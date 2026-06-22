from django.urls import path

from .views import cancel_views, mp_views, paypal_views

urlpatterns = [
    # Cancelación de suscripción
    path('cancelar/', cancel_views.cancelar_vista, name='pago_cancelar'),
    path('cancelar/confirmar/', cancel_views.cancelar_confirmar, name='pago_cancelar_confirmar'),

    # PayPal — suscripciones
    path('paypal/suscribir/<str:plan>/', paypal_views.suscribir, name='pago_paypal_suscribir'),
    path('paypal/retorno/', paypal_views.retorno_suscripcion, name='pago_paypal_retorno'),
    path('paypal/webhook/', paypal_views.webhook, name='pago_paypal_webhook'),
    # PayPal — packs (retorno ANTES del parámetro variable)
    path('paypal/pack/retorno/', paypal_views.retorno_pack, name='pago_paypal_pack_retorno'),
    path('paypal/pack/<str:slug>/', paypal_views.pack, name='pago_paypal_pack'),
    # PayPal — AJAX para crear orden (SDK Buttons createOrder)
    path('paypal/api/orden/<str:slug>/', paypal_views.api_orden_pack, name='pago_paypal_api_orden'),

    # MercadoPago — suscripciones
    path('mp/suscribir/<str:plan>/', mp_views.suscribir, name='pago_mp_suscribir'),
    path('mp/retorno/suscripcion/', mp_views.retorno_suscripcion, name='pago_mp_retorno_suscripcion'),
    path('mp/webhook/', mp_views.webhook, name='pago_mp_webhook'),
    # MercadoPago — packs (retorno ANTES del parámetro variable)
    path('mp/pack/retorno/', mp_views.retorno_pack, name='pago_mp_pack_retorno'),
    path('mp/pack/<str:slug>/', mp_views.pack, name='pago_mp_pack'),
    # MercadoPago — AJAX para crear preferencia (Wallet Brick)
    path('mp/api/preferencia/<str:slug>/', mp_views.api_preferencia_pack, name='pago_mp_api_preferencia'),
]
