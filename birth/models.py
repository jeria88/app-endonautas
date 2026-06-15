from django.conf import settings
from django.db import models


class BirthData(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='birth_data', null=True, blank=True
    )
    temp_profile = models.OneToOneField(
        'practitioners.TemporaryProfile', on_delete=models.CASCADE,
        related_name='birth_data', null=True, blank=True
    )
    birth_date = models.DateField()
    birth_time = models.TimeField(null=True, blank=True)
    city = models.CharField(max_length=150)
    country = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timezone_str = models.CharField(max_length=60, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        who = self.user.email if self.user else str(self.temp_profile)
        return f'{who} — {self.birth_date} {self.city}'


class BirthReport(models.Model):
    TYPE_CHOICES = [
        ('astral', 'Carta Astral'),
        ('hd', 'Human Design'),
        ('saju', 'Saju / BaZi'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('done', 'Listo'),
        ('error', 'Error'),
    ]

    birth_data = models.ForeignKey(BirthData, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    raw_data = models.JSONField(default=dict, blank=True)
    ai_reading = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('birth_data', 'report_type')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.birth_data} — {self.get_report_type_display()} [{self.status}]'
