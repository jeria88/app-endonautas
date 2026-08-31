from django.conf import settings
from django.db import models

from .constants import PLANS, PRODUCTS, TALLERES


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
    """Histórico. Los packs ya no se venden: la moneda murió en ddba5b8 y su
    checkout se retiró. El modelo queda para no perder las compras pasadas."""

    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [('pending', 'Pendiente'), ('paid', 'Pagado'), ('failed', 'Fallido')]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fractone_packs'
    )
    gateway = models.CharField(max_length=10)
    pack_slug = models.CharField(max_length=20)
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


class EbookOrder(models.Model):
    """Compra única del ebook (checkout de invitado, mismo patrón que TallerReserva).
    Soporta MP (CLP) y PayPal (USD). download_token se genera al confirmar el pago."""
    PRODUCT_CHOICES = [(k, v['title']) for k, v in PRODUCTS.items()]

    GATEWAY_CHOICES = [('paypal', 'PayPal'), ('mp', 'MercadoPago')]

    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_DELIVERED = 'delivered'
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('failed', 'Fallido'),
        ('delivered', 'Entregado'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ebook_orders'
    )
    product_slug = models.CharField(max_length=40, choices=PRODUCT_CHOICES, default='endonautica-ebook')
    gateway = models.CharField(max_length=10, choices=GATEWAY_CHOICES)
    amount_local = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    gateway_payment_id = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    canal_origen = models.CharField(max_length=40, blank=True)
    download_token = models.CharField(max_length=64, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['gateway', 'gateway_payment_id']),
            models.Index(fields=['download_token']),
        ]

    def __str__(self):
        return f'{self.user.email} — ebook via {self.gateway} ({self.status})'


class EbookLead(models.Model):
    """Captura post-test de heridas: quien pidió el PDF de su herida, con o sin compra
    posterior. lead→contacto→pago(EbookOrder)→entrega, CRM mínimo vía Django admin."""
    STATUS_NUEVO = 'nuevo'
    STATUS_PDF_ENTREGADO = 'pdf_entregado'
    STATUS_CONTACTADO = 'contactado'
    STATUS_COMPRADO = 'comprado'
    STATUS_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('pdf_entregado', 'PDF entregado'),
        ('contactado', 'Contactado'),
        ('comprado', 'Comprado'),
    ]

    email = models.EmailField(blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    herida = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nuevo')
    canal_origen = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.email or self.whatsapp} — {self.herida} ({self.status})'


class EbookFunnelEmail(models.Model):
    """Un email de la campaña del ebook ya enviado a una dirección. La unicidad
    (email, step) es la idempotencia del comando `run_ebook_funnel`: si la fila
    existe, ese paso no se vuelve a mandar. Los pasos T1/P1 no se registran acá —
    salen inline desde las views y no los toca el comando."""
    STEP_CHOICES = [
        ('T2', 'Test · ciclo de control (+2d)'),
        ('T3', 'Test · inercia e invitación (+4d)'),
        ('A1', 'Carrito · a la hora'),
        ('A2', 'Carrito · a las 24 h'),
        ('P2', 'Post-compra · resistencia (+3d)'),
        ('P3', 'Post-compra · el mapa no es el territorio (+7d)'),
    ]

    email = models.EmailField()
    step = models.CharField(max_length=2, choices=STEP_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        constraints = [
            models.UniqueConstraint(fields=['email', 'step'], name='funnel_email_una_vez_por_paso'),
        ]

    def __str__(self):
        return f'{self.email} — {self.step} ({self.sent_at:%Y-%m-%d})'


class EbookOptOut(models.Model):
    """Baja de la campaña del ebook. El comando `run_ebook_funnel` no manda ningún
    paso a un email que esté acá. No afecta la entrega del libro (P1) ni el PDF del
    test (T1): esos son transaccionales, respuesta directa a una acción del usuario."""
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email
