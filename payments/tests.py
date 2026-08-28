"""Guardas contra el regreso de la economía de Fractones.

Fractones fue reemplazada por el modelo feature-based por plan en ddba5b8
(2026-06-22), pero sobrevivió un año en dos lugares que sí eran alcanzables:
la página `endonautas.cl/fractones/` y las rutas de compra de packs, que
cobraban por una moneda que la app ya no gasta en ninguna parte.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import SimpleTestCase, TestCase
from django.urls import NoReverseMatch, reverse

from .models import EbookOrder
from .views.ebook_views import _marcar_pagado
from .views.entrega import entregar_ebook
from .views.taller_views import _get_or_create_user


class FractonesNoVuelve(SimpleTestCase):
    def test_no_hay_checkout_de_packs(self):
        """Ninguna pasarela debe poder cobrar un pack de Fractones."""
        for nombre in (
            'pago_mp_pack', 'pago_mp_pack_retorno', 'pago_mp_api_preferencia',
            'pago_paypal_pack', 'pago_paypal_pack_retorno', 'pago_paypal_api_orden',
        ):
            with self.assertRaises(NoReverseMatch, msg=f'{nombre} volvió a existir'):
                reverse(nombre)

    def test_constants_no_define_precios_de_packs(self):
        from payments import constants
        self.assertFalse(hasattr(constants, 'PACKS'))

    def test_checkout_de_suscripcion_sigue_resolviendo(self):
        """Las vistas de cobro hacen `reverse()` en runtime: `manage.py check` no
        las ve. Al retirar /tokens/ el checkout apuntaba a una ruta muerta."""
        self.assertEqual(reverse('planes'), '/planes/')
        for nombre, args in (
            ('pago_mp_suscribir', ['navegante']),
            ('pago_paypal_suscribir', ['practicante']),
            ('pago_mp_webhook', []), ('pago_paypal_webhook', []),
            ('pago_cancelar', []),
        ):
            reverse(nombre, args=args)

    def test_planes_publicos_son_los_dos_reales(self):
        """`empresa` no se ofrece: se hará a pedido de un cliente real."""
        from payments.constants import PLANS
        self.assertEqual(set(PLANS), {'navegante', 'practicante'})


class EntregaDelEbook(TestCase):
    """El comprador tiene que recibir un link que funcione, venga o no de un request.

    Los dos caminos que confirman la compra son distintos: el retorno del navegador
    trae `request` y el webhook de MP no. Sin el fallback a APP_BASE_URL, el segundo
    manda un href relativo — el email llega, el libro no.
    """

    def setUp(self):
        self.user = get_user_model().objects.create(email='comprador@test.cl')
        self.order = EbookOrder.objects.create(
            user=self.user, gateway='mp', amount_local=17000, currency='CLP',
            status=EbookOrder.STATUS_PAID, download_token='t' * 48,
        )

    def test_link_absoluto_sin_request(self):
        self.assertTrue(entregar_ebook(self.order, request=None))
        self.assertEqual(len(mail.outbox), 1)
        cuerpo = mail.outbox[0].body
        self.assertIn(f'{settings.APP_BASE_URL}/pago/ebook/descargar/', cuerpo)
        self.assertNotIn('href="/pago', mail.outbox[0].alternatives[0][0])

    def test_marcar_pagado_es_idempotente(self):
        """Webhook y retorno pueden llegar los dos: el segundo no debe re-entregar."""
        _marcar_pagado(self.order, 'pay-1')
        self.assertEqual(len(mail.outbox), 1)
        # El segundo camino filtra por status=PENDING y ya no encuentra la orden.
        pendientes = EbookOrder.objects.filter(
            user=self.user, gateway='mp', status=EbookOrder.STATUS_PENDING,
        )
        self.assertEqual(pendientes.count(), 0)

    def test_comprar_no_manda_mail_de_contrasena(self):
        """El comprador solo recibe el libro — el mail de 'restablece tu contraseña'
        confunde a quien nunca pidió una cuenta."""
        _get_or_create_user(None, 'nuevo@test.cl', send_setup=False)
        self.assertEqual(len(mail.outbox), 0)
