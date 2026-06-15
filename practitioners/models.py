import uuid
from django.conf import settings
from django.db import models


class TemporaryProfile(models.Model):
    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='client_profiles'
    )
    claimed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='claimed_profile'
    )
    alias = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    access_code = models.UUIDField(default=uuid.uuid4, unique=True)
    notes = models.TextField(blank=True)
    clinical_summary = models.TextField(blank=True)
    assigned_tests = models.ManyToManyField('psychometrics.Test', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.alias} ({self.practitioner.email})'


class SessionNote(models.Model):
    profile = models.ForeignKey(TemporaryProfile, on_delete=models.CASCADE, related_name='session_notes')
    practitioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    session_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-session_date']

    def __str__(self):
        return f'{self.profile.alias} — {self.session_date}'


class TherapySession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ]
    TYPE_CHOICES = [
        ('online', 'Online'),
        ('presencial', 'Presencial'),
    ]

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='therapy_sessions'
    )
    profile = models.ForeignKey(TemporaryProfile, on_delete=models.CASCADE, related_name='sessions')
    datetime = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    session_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='online')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    meeting_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return f'{self.profile.alias} — {self.datetime:%Y-%m-%d %H:%M} [{self.status}]'


class Availability(models.Model):
    DAY_CHOICES = [(i, d) for i, d in enumerate(
        ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    )]

    practitioner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='availability'
    )
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('practitioner', 'day_of_week', 'start_time')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f'{self.practitioner.email} — {self.get_day_of_week_display()} {self.start_time}-{self.end_time}'
