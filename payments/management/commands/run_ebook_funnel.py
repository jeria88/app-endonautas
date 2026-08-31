"""Motor de la campaña de emails del ebook. Cron cada 30 min en el host Oracle.

Recorre las 3 ramas en orden de precedencia. La idempotencia real vive en
`funnel_emails._send` (reclama `EbookFunnelEmail(email, step)` antes de mandar);
acá solo se decide a quién le toca cada paso.

Precedencia (regla anti-nag, decidida con Franco 2026-08-31):
  - compró  → arranca post-compra (C); carrito y test no aplican
  - inició checkout (EbookOrder pending) → carrito (B); el test se corta para siempre
  - solo hizo el test → nutrición del test (A)
"""
import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from payments import funnel_emails as fe
from payments.models import EbookLead, EbookOrder
from payments.services import paypal as paypal_service
from payments.views.ebook_views import _marcar_pagado

logger = logging.getLogger(__name__)

PAID_STATES = [EbookOrder.STATUS_PAID, EbookOrder.STATUS_DELIVERED]


class Command(BaseCommand):
    help = 'Envía los emails diferidos de la campaña del ebook.'

    def handle(self, *args, **opts):
        now = timezone.now()
        r = {}

        r['paypal_reconciliado'] = self._reconciliar_paypal(now)

        # Rama C · post-compra
        r['P2'] = self._post_compra('P2', now - timedelta(days=3), now - timedelta(days=30), fe.enviar_P2)
        r['P3'] = self._post_compra('P3', now - timedelta(days=7), now - timedelta(days=30), fe.enviar_P3)

        # Rama B · carrito abandonado
        r['A1'] = self._carrito('A1', now - timedelta(hours=1), now - timedelta(days=3), fe.enviar_A1)
        r['A2'] = self._carrito('A2', now - timedelta(hours=24), now - timedelta(days=4), fe.enviar_A2)

        # Rama A · nutrición del test
        r['T2'] = self._test('T2', now - timedelta(days=2), now - timedelta(days=30), fe.enviar_T2)
        r['T3'] = self._test('T3', now - timedelta(days=4), now - timedelta(days=30), fe.enviar_T3)

        self.stdout.write(f'[run_ebook_funnel] {now:%Y-%m-%d %H:%M} {r}')

    # -- PayPal: pagó y cerró la pestaña -> orden pending nunca capturada/entregada --
    def _reconciliar_paypal(self, now):
        n = 0
        orders = EbookOrder.objects.filter(
            gateway='paypal', status=EbookOrder.STATUS_PENDING,
            created_at__gte=now - timedelta(days=3),
        ).select_related('user')
        for o in orders:
            if not o.gateway_payment_id:
                continue
            try:
                data = paypal_service.get_order(o.gateway_payment_id)
                estado = data.get('status')
                if estado == 'APPROVED':
                    cap = paypal_service.capture_order(o.gateway_payment_id)
                    if cap.get('status') != 'COMPLETED':
                        continue
                elif estado != 'COMPLETED':
                    continue
                # claim: solo el primero que la pase de PENDING la entrega
                if EbookOrder.objects.filter(pk=o.pk, status=EbookOrder.STATUS_PENDING).update(
                        status=EbookOrder.STATUS_PAID):
                    o.refresh_from_db()
                    _marcar_pagado(o, o.gateway_payment_id)
                    n += 1
            except Exception as e:
                logger.error(f'run_ebook_funnel paypal reconcile order={o.pk}: {e}')
        return n

    def _post_compra(self, step, hasta, desde, fn):
        n = 0
        qs = EbookOrder.objects.filter(
            status=EbookOrder.STATUS_DELIVERED,
            delivered_at__lte=hasta, delivered_at__gte=desde,
        ).select_related('user')
        for o in qs:
            if fn(o):
                n += 1
        return n

    def _carrito(self, step, hasta, desde, fn):
        n, vistos = 0, set()
        qs = EbookOrder.objects.filter(
            status=EbookOrder.STATUS_PENDING,
            created_at__lte=hasta, created_at__gte=desde,
        ).select_related('user').order_by('-created_at')
        for o in qs:
            email = (o.user.email or '').lower()
            if not email or email in vistos:
                continue
            vistos.add(email)
            if EbookOrder.objects.filter(user=o.user, status__in=PAID_STATES).exists():
                continue  # compró en otra orden -> no es carrito abandonado
            if fn(o):
                n += 1
        return n

    def _test(self, step, hasta, desde, fn):
        n, vistos = 0, set()
        qs = (EbookLead.objects
              .filter(created_at__lte=hasta, created_at__gte=desde)
              .exclude(email='').exclude(herida='')
              .order_by('-created_at'))
        for lead in qs:
            email = (lead.email or '').lower()
            if not email or email in vistos:
                continue
            vistos.add(email)
            if lead.status == EbookLead.STATUS_COMPRADO:
                continue
            # cualquier EbookOrder (pending o pagada) para ese email -> pasó a rama B o C
            if EbookOrder.objects.filter(user__email__iexact=email).exists():
                continue
            if fn(lead):
                n += 1
        return n
