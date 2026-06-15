from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Test(models.Model):
    DIMENSION_CHOICES = [
        ('identidad', 'Identidad'),
        ('emociones', 'Emociones'),
        ('cuerpo', 'Cuerpo'),
        ('vinculos', 'Vínculos'),
        ('sombra', 'Sombra'),
        ('espiritualidad', 'Espiritualidad'),
        ('suenos', 'Sueños'),
        ('proposito', 'Propósito'),
        ('comunidad', 'Comunidad'),
        ('abundancia', 'Abundancia'),
        ('creatividad', 'Creatividad'),
        ('mente', 'Mente'),
    ]
    INSTRUMENT_CHOICES = [
        ('clinical', 'Clínico validado'),
        ('adapted', 'Adaptado'),
        ('custom', 'Endonauta'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    dimension = models.CharField(max_length=20, choices=DIMENSION_CHOICES)
    instrument_type = models.CharField(max_length=20, choices=INSTRUMENT_CHOICES, default='adapted')
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    estimated_minutes = models.IntegerField(default=5)
    token_cost = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(models.Model):
    SCALE_CHOICES = [
        ('likert5', 'Likert 1-5 frecuencia'),
        ('likert5a', 'Likert 1-5 acuerdo'),
        ('likert4', 'Likert 0-4'),
        ('likert3', 'Likert 0-3'),
        ('likert7', 'Likert 1-7'),
        ('binary', 'Sí/No'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    dimension_key = models.CharField(max_length=50, blank=True)
    scale = models.CharField(max_length=20, choices=SCALE_CHOICES, default='likert5')
    reverse_scored = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'[{self.test.slug}] {self.text[:60]}'


class TestResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='test_results', null=True, blank=True
    )
    temp_profile = models.ForeignKey(
        'practitioners.TemporaryProfile', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='temp_test_results'
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    raw_scores = models.JSONField(default=dict)
    evaluation = models.JSONField(default=dict)
    ai_insight = models.TextField(blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        who = self.user.email if self.user else str(self.temp_profile)
        return f'{who} — {self.test.name}'
