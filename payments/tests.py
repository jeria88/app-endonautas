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

from datetime import timedelta
from unittest import mock

from django.core.management import call_command
from django.utils import timezone

from .models import EbookFunnelEmail, EbookLead, EbookOptOut, EbookOrder
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

    def test_entrega_los_dos_formatos(self):
        """Mucha gente no tiene lector de EPUB: si el correo solo trae ese
        formato, el libro no se abre y el reembolso es cuestión de tiempo."""
        entregar_ebook(self.order, request=None)
        cuerpo = mail.outbox[0].body
        self.assertIn(f'/{self.order.download_token}/pdf/', cuerpo)
        self.assertIn(f'/{self.order.download_token}/epub/', cuerpo)

    def test_descarga_por_formato(self):
        from payments.views.entrega import FORMATOS
        for formato, (_, nombre, tipo) in FORMATOS.items():
            r = self.client.get(reverse(
                'descargar_ebook_formato', args=[self.order.download_token, formato]))
            self.assertEqual(r.status_code, 200, formato)
            self.assertEqual(r['Content-Type'], tipo)
            self.assertIn(nombre, r['Content-Disposition'])
        # El link viejo, sin formato, sigue entregando el EPUB: hay correos ya
        # enviados con esa forma de URL.
        r = self.client.get(reverse('descargar_ebook', args=[self.order.download_token]))
        self.assertEqual(r.status_code, 200)
        self.assertIn('Endonautica.epub', r['Content-Disposition'])

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


class MetaCapiEnvioDePurchase(TestCase):
    """CAPI es redundante al pixel — nunca debe romper la entrega del libro si
    falla, y el payload tiene que traer lo que Meta necesita para deduplicar
    contra el evento client-side y atribuir la venta."""

    def setUp(self):
        self.user = get_user_model().objects.create(email='comprador@test.cl')
        self.order = EbookOrder.objects.create(
            user=self.user, gateway='mp', amount_local=17000, currency='CLP',
            status=EbookOrder.STATUS_PAID, download_token='t' * 48,
        )

    @mock.patch('payments.services.meta_capi.requests.post')
    def test_sin_token_no_llama_a_la_red(self, mock_post):
        from payments.services import meta_capi
        meta_capi.send_purchase(self.order)
        mock_post.assert_not_called()

    @mock.patch('payments.services.meta_capi.requests.post')
    def test_payload_correcto(self, mock_post):
        from payments.services import meta_capi
        mock_post.return_value = mock.Mock(status_code=200)
        with self.settings(META_CAPI_ACCESS_TOKEN='tok', META_PIXEL_ID='860717205439662'):
            meta_capi.send_purchase(self.order)
        self.assertTrue(mock_post.called)
        payload = mock_post.call_args.kwargs['json']['data'][0]
        self.assertEqual(payload['event_name'], 'Purchase')
        self.assertEqual(payload['event_id'], f'purchase-{self.order.pk}')
        self.assertEqual(payload['custom_data']['value'], 17000.0)
        self.assertEqual(payload['custom_data']['currency'], 'CLP')
        self.assertEqual(payload['user_data']['em'], [meta_capi._hash('comprador@test.cl')])

    @mock.patch('payments.services.meta_capi.requests.post')
    def test_marcar_pagado_no_revienta_si_capi_falla(self, mock_post):
        mock_post.side_effect = Exception('timeout de la API de Meta')
        with self.settings(META_CAPI_ACCESS_TOKEN='tok'):
            _marcar_pagado(self.order, 'pay-1')
        self.assertEqual(len(mail.outbox), 1)  # el libro se entrega igual


class ResultadoVisibleParaInvitados(TestCase):
    """El checkout del ebook y la seña del taller son de invitado, pero base.html
    solo renderiza `content` si el usuario está autenticado. Sin `public_content`
    el comprador pagaba y veía una página en blanco — pasó en producción."""

    def test_anonimo_ve_el_resultado(self):
        r = self.client.get(reverse('pago_ebook_retorno_mp'), {'status': 'failure'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Algo salió mal')

    def test_anonimo_ve_el_boton_de_descarga(self):
        user = get_user_model().objects.create(email='invitado@test.cl')
        order = EbookOrder.objects.create(
            user=user, gateway='mp', amount_local=16990, currency='CLP',
            status=EbookOrder.STATUS_PAID, download_token='d' * 48,
        )
        # La vista de retorno exige llamar a MercadoPago, así que se renderiza el
        # template directo con el mismo contexto que arma retorno_mp en el éxito.
        from django.template.loader import render_to_string
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        html = render_to_string('payments/resultado.html', {
            'exito': True, 'gateway': 'MercadoPago',
            'mensaje': 'Pago confirmado. Aquí está tu libro.',
            'download_url': f'https://app.endonautas.cl/pago/ebook/descargar/{order.download_token}/',
        }, request=req)
        self.assertIn('Descargar el libro', html)
        self.assertIn(order.download_token, html)


class CampanaDelEbook(TestCase):
    """`run_ebook_funnel` — las 3 ramas, la precedencia anti-nag y la idempotencia."""

    def _lead(self, email, herida='abandono', edad_dias=5, status=EbookLead.STATUS_PDF_ENTREGADO):
        lead = EbookLead.objects.create(email=email, herida=herida, status=status)
        EbookLead.objects.filter(pk=lead.pk).update(
            created_at=timezone.now() - timedelta(days=edad_dias))
        return lead

    def _order(self, email, status, edad_horas=0, gateway='mp', delivered_hace_dias=None):
        user, _ = get_user_model().objects.get_or_create(email=email)
        o = EbookOrder.objects.create(
            user=user, gateway=gateway, amount_local=16990, currency='CLP', status=status,
            download_token=('x' * 48) if status != EbookOrder.STATUS_PENDING else '',
        )
        campos = {}
        if edad_horas:
            campos['created_at'] = timezone.now() - timedelta(hours=edad_horas)
        if delivered_hace_dias is not None:
            campos['delivered_at'] = timezone.now() - timedelta(days=delivered_hace_dias)
        if campos:
            EbookOrder.objects.filter(pk=o.pk).update(**campos)
        return EbookOrder.objects.get(pk=o.pk)

    def test_carrito_manda_el_test_se_corta(self):
        """Si hay una EbookOrder para ese email (aunque sea pending), la nutrición
        del test no le manda nada — recibe el carrito."""
        self._lead('dobles@test.cl', edad_dias=5)
        self._order('dobles@test.cl', EbookOrder.STATUS_PENDING, edad_horas=2)
        call_command('run_ebook_funnel')
        pasos = set(EbookFunnelEmail.objects.filter(email='dobles@test.cl')
                    .values_list('step', flat=True))
        self.assertIn('A1', pasos)
        self.assertNotIn('T2', pasos)
        self.assertNotIn('T3', pasos)

    def test_comprador_no_recibe_carrito_ni_test(self):
        self._lead('compro@test.cl', edad_dias=6)
        self._order('compro@test.cl', EbookOrder.STATUS_PENDING, edad_horas=30)   # una pending vieja
        self._order('compro@test.cl', EbookOrder.STATUS_DELIVERED, delivered_hace_dias=1)
        call_command('run_ebook_funnel')
        pasos = set(EbookFunnelEmail.objects.filter(email='compro@test.cl')
                    .values_list('step', flat=True))
        self.assertEqual(pasos & {'A1', 'A2', 'T2', 'T3'}, set())

    def test_post_compra_por_antiguedad(self):
        self._order('lector@test.cl', EbookOrder.STATUS_DELIVERED, delivered_hace_dias=1)
        call_command('run_ebook_funnel')
        self.assertFalse(EbookFunnelEmail.objects.filter(email='lector@test.cl').exists())
        EbookOrder.objects.filter(user__email='lector@test.cl').update(
            delivered_at=timezone.now() - timedelta(days=4))
        call_command('run_ebook_funnel')
        pasos = set(EbookFunnelEmail.objects.filter(email='lector@test.cl')
                    .values_list('step', flat=True))
        self.assertEqual(pasos, {'P2'})

    def test_nutricion_del_test_personalizada(self):
        self._lead('curioso@test.cl', herida='traicion', edad_dias=5)
        call_command('run_ebook_funnel')
        pasos = set(EbookFunnelEmail.objects.filter(email='curioso@test.cl')
                    .values_list('step', flat=True))
        self.assertEqual(pasos, {'T2', 'T3'})
        cuerpos = ' '.join(m.body for m in mail.outbox)
        self.assertIn('traición', cuerpos.lower())
        self.assertIn('Controladora', cuerpos)

    def test_idempotente(self):
        self._lead('repe@test.cl', edad_dias=5)
        call_command('run_ebook_funnel')
        n1 = len(mail.outbox)
        call_command('run_ebook_funnel')
        self.assertEqual(len(mail.outbox), n1)
        self.assertEqual(
            EbookFunnelEmail.objects.filter(email='repe@test.cl', step='T2').count(), 1)

    def test_optout_corta_todo(self):
        EbookOptOut.objects.create(email='fuera@test.cl')
        self._lead('fuera@test.cl', edad_dias=5)
        self._order('nada@test.cl', EbookOrder.STATUS_DELIVERED, delivered_hace_dias=8)
        EbookOptOut.objects.create(email='nada@test.cl')
        call_command('run_ebook_funnel')
        self.assertFalse(EbookFunnelEmail.objects.exists())

    def test_franco_excluido(self):
        self._lead(settings.FRANCO_EMAIL, edad_dias=5)
        call_command('run_ebook_funnel')
        self.assertFalse(EbookFunnelEmail.objects.exists())

    def test_baja_desde_token_firmado(self):
        from django.core import signing
        from payments.funnel_emails import BAJA_SALT
        token = signing.dumps('adios@test.cl', salt=BAJA_SALT)
        r = self.client.get(reverse('pago_ebook_baja', args=[token]))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(EbookOptOut.objects.filter(email='adios@test.cl').exists())
        # one-click POST no revienta por CSRF
        r2 = self.client.post(reverse('pago_ebook_baja', args=[token]))
        self.assertEqual(r2.status_code, 200)
