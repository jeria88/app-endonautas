from django.conf import settings
from django.db import models

from .constants import PACKS, PLANS, TALLERES


class Subscription(models.Model):
    GATEWAY_PAYPAL = 'paypal'
    GATEWAY_MP = 'mp'
    GATEWAY_CHOICES = [('paypal', 'PayPal'), ('mp', 'MercadoPago')]

    PLAN_CHOICES = [(k, v['title']) for k, v in PLANS.items()]

    STATUS_PENDING = 'pending'
    STATUS_ACTIVE = 'active'
    STATUS_PAUSED = 'paused'
    STATUS_CANCELLED = 'cancelled'
    STATUS_EXPIRED = 'expired'
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('active', 'Activa'),
        ('paused', 'Pausada'),
        ('cancelled', 'Cancelada'),
        ('expired', 'Vencida'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions'
    )
    gateway = models.CharField(max_length=10, choices=GATEWAY_CHOICES)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    gateway_subscription_id = models.CharField(max_length=200, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    next_billing_date = models.DateField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['gateway', 'gateway_subscription_id']),
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f'{self.user.email} — {self.plan} via {self.gateway} ({self.status})'


class FractonesPack(models.Model):
    PACK_CHOICES = [(k, v['title']) for k, v in PACKS.items()]

    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [('pending', 'Pendiente'), ('paid', 'Pagado'), ('failed', 'Fallido')]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fractone_packs'
    )
    gateway = models.CharField(max_length=10)
    pack_slug = models.CharField(max_length=20, choices=PACK_CHOICES)
    fractones = models.IntegerField()
    amount_local = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    gateway_payment_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['gateway', 'gateway_payment_id']),
        ]

    def __str__(self):
        return f'{self.user.email} — {self.pack_slug} via {self.gateway} ({self.status})'


class TallerReserva(models.Model):
    """Seña de reserva de cupo para un taller presencial (pago único). Resto se paga presencial."""
    TALLER_CHOICES = [(k, v['title']) for k, v in TALLERES.items()]

    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [('pending', 'Pendiente'), ('paid', 'Pagado'), ('failed', 'Fallido')]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taller_reservas'
    )
    gateway = models.CharField(max_length=10)
    taller_slug = models.CharField(max_length=40, choices=TALLER_CHOICES)
    amount_local = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    gateway_payment_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['gateway', 'gateway_payment_id']),
        ]

    def __str__(self):
        return f'{self.user.email} — {self.taller_slug} via {self.gateway} ({self.status})'
