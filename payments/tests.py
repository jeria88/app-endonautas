"""Guardas contra el regreso de la economía de Fractones.

Fractones fue reemplazada por el modelo feature-based por plan en ddba5b8
(2026-06-22), pero sobrevivió un año en dos lugares que sí eran alcanzables:
la página `endonautas.cl/fractones/` y las rutas de compra de packs, que
cobraban por una moneda que la app ya no gasta en ninguna parte.
"""
from django.test import SimpleTestCase
from django.urls import NoReverseMatch, reverse


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
