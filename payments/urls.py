from django.urls import path

from .views import bono_views, cancel_views, ebook_views, entrega, mp_views, paypal_views, taller_views

urlpatterns = [
    # Cancelación de suscripción
    path('cancelar/', cancel_views.cancelar_vista, name='pago_cancelar'),
    path('cancelar/confirmar/', cancel_views.cancelar_confirmar, name='pago_cancelar_confirmar'),

    # PayPal — suscripciones
    path('paypal/suscribir/<str:plan>/', paypal_views.suscribir, name='pago_paypal_suscribir'),
    path('paypal/retorno/', paypal_views.retorno_suscripcion, name='pago_paypal_retorno'),
    path('paypal/webhook/', paypal_views.webhook, name='pago_paypal_webhook'),
    # MercadoPago — suscripciones
    path('mp/suscribir/<str:plan>/', mp_views.suscribir, name='pago_mp_suscribir'),
    path('mp/retorno/suscripcion/', mp_views.retorno_suscripcion, name='pago_mp_retorno_suscripcion'),
    path('mp/webhook/', mp_views.webhook, name='pago_mp_webhook'),
    # MercadoPago — seña de taller (checkout de invitado, sin cuenta previa)
    path('mp/taller/retorno/', taller_views.retorno, name='pago_mp_taller_retorno'),
    path('mp/taller/<str:slug>/', taller_views.reservar, name='pago_mp_taller_reservar'),

    # MercadoPago — bono taller (QR post-taller, mes gratis Plan Practicante)
    path('mp/bono-taller/retorno/', bono_views.retorno, name='pago_mp_bono_taller_retorno'),
    path('mp/bono-taller/', bono_views.activar, name='pago_mp_bono_taller'),

    # Ebook Endonautica — lead post-test, checkout de invitado (MP + PayPal)
    path('ebook/lead/', ebook_views.lead, name='pago_ebook_lead'),
    path('ebook/comprar/<str:gateway>/', ebook_views.comprar, name='pago_ebook_comprar'),
    path('ebook/retorno/mp/', ebook_views.retorno_mp, name='pago_ebook_retorno_mp'),
    path('ebook/retorno/paypal/', ebook_views.retorno_paypal, name='pago_ebook_retorno_paypal'),
    path('ebook/descargar/<str:token>/', entrega.descargar_ebook, name='descargar_ebook'),
]
