"""Avisos al harness de ACME Agents desde los planes de la app (Navegante / Practicante).

Un solo punto para las 4 vistas que tocan suscripciones (MP y PayPal, retorno y webhook):
  - Subscription creada en 'pending'        → checkout_iniciado
  - Subscription que pasa a 'active'         → venta (monto del plan; USD convertido a CLP solo
                                              para el embudo, el original viaja en datos)
Solo se dispara con save(); la app no activa suscripciones con queryset.update().
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .constants import PLANS
from .models import Subscription
from .services import harness


@receiver(pre_save, sender=Subscription)
def _recordar_estado(sender, instance, **kwargs):
    instance._estado_previo = (
        Subscription.objects.filter(pk=instance.pk).values_list('status', flat=True).first()
        if instance.pk else None
    )


@receiver(post_save, sender=Subscription)
def _avisar_harness(sender, instance, created, **kwargs):
    plan = PLANS.get(instance.plan, {})
    contacto = {'email': instance.user.email, 'nombre': instance.user.first_name or None,
                'fuente': 'app-planes'}
    datos = {'producto': f'plan-{instance.plan}', 'pasarela': instance.gateway}
    if created and instance.status == Subscription.STATUS_PENDING:
        harness.emitir('checkout_iniciado', contacto, datos=datos,
                       dedupe_key=f'sub-{instance.pk}-checkout')
    elif instance.status == Subscription.STATUS_ACTIVE and getattr(instance, '_estado_previo', None) != 'active':
        es_clp = instance.gateway == Subscription.GATEWAY_MP
        monto = plan.get('price_clp') if es_clp else harness.a_clp(plan.get('price_usd', '0'), 'USD')
        harness.emitir('venta', contacto, monto_clp=monto,
                       datos={**datos, 'external_ref': instance.gateway_subscription_id or f'sub-{instance.pk}',
                              'moneda': 'CLP' if es_clp else 'USD',
                              'monto_original': str(plan.get('price_clp') if es_clp else plan.get('price_usd'))},
                       dedupe_key=f'sub-{instance.pk}-venta', atribucion='externo:app-planes')
