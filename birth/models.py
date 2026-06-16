from django.conf import settings
from django.db import models


SIGN_ES = {
    'Ari': 'Aries', 'Tau': 'Tauro', 'Gem': 'Géminis', 'Can': 'Cáncer',
    'Leo': 'Leo', 'Vir': 'Virgo', 'Lib': 'Libra', 'Sco': 'Escorpio',
    'Sag': 'Sagitario', 'Cap': 'Capricornio', 'Aqu': 'Acuario', 'Pis': 'Piscis',
}

HOUSE_NUM = {
    'First_House': 1, 'Second_House': 2, 'Third_House': 3, 'Fourth_House': 4,
    'Fifth_House': 5, 'Sixth_House': 6, 'Seventh_House': 7, 'Eighth_House': 8,
    'Ninth_House': 9, 'Tenth_House': 10, 'Eleventh_House': 11, 'Twelfth_House': 12,
}

SIGN_ELEMENT = {
    'Aries': 'fire', 'Leo': 'fire', 'Sagitario': 'fire',
    'Tauro': 'earth', 'Virgo': 'earth', 'Capricornio': 'earth',
    'Géminis': 'air', 'Libra': 'air', 'Acuario': 'air',
    'Cáncer': 'water', 'Escorpio': 'water', 'Piscis': 'water',
}


class BirthData(models.Model):
    GENDER_CHOICES = [('M', 'Masculino'), ('F', 'Femenino')]

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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
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
