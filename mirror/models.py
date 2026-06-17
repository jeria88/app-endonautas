from django.conf import settings
from django.db import models


class KnowledgeChunk(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=150, blank=True)
    source = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    embedding = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title[:60]} ({self.author})'


class ChatSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=200, blank=True)
    conflict_summary = models.TextField(blank=True)
    return_question = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.email} — {self.title or self.pk}'


class ChatMessage(models.Model):
    ROLE_CHOICES = [('user', 'Usuario'), ('assistant', 'Espejo')]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    sources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'[{self.role}] {self.content[:60]}'


class DreamEntry(models.Model):
    NAUMINTO_CHOICES = [
        ('literal', 'Literal'),
        ('simbolico', 'Simbólico'),
        ('profetico', 'Profético'),
        ('lucido', 'Lúcido'),
        ('recurrente', 'Recurrente'),
        ('arquetipico', 'Arquetípico'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dreams')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_lucid = models.BooleanField(default=False)
    dream_date = models.DateField()
    tags = models.CharField(max_length=200, blank=True)
    reality_check = models.BooleanField(default=False)
    nauminto_type = models.CharField(max_length=20, choices=NAUMINTO_CHOICES, blank=True)
    archetype_tags = models.JSONField(default=list, blank=True)
    ai_insight = models.TextField(blank=True)
    is_nauminto = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dream_date', '-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.title or str(self.dream_date)}'


class BitacoraEntry(models.Model):
    ENTRY_TYPES = [
        # Categorías manuales (el usuario elige)
        ('sueno', 'Sueño'),
        ('sombra', 'Sombra'),
        ('patron', 'Patrón'),
        ('signo', 'Signo o síntoma'),
        ('manual', 'Nota libre'),
        # Auto-generadas por el sistema
        ('auto_test', 'Test completado'),
        ('auto_espejo', 'Sesión Espejo'),
        ('auto_terapeuta', 'Consulta Terapéutica'),
        ('auto_oraculo', 'Oráculo consultado'),
        ('auto_regulacion', 'Ejercicio de regulación'),
        ('auto_dream', 'Sueño registrado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bitacora')
    entry_type = models.CharField(max_length=30, choices=ENTRY_TYPES, default='manual')
    content = models.TextField()
    tags = models.CharField(max_length=200, blank=True)
    emoji = models.CharField(max_length=10, blank=True)
    fecha = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} [{self.entry_type}] {self.fecha}'


class EjercicioRegulacion(models.Model):
    CATEGORY_CHOICES = [
        ('respiracion', 'Respiración'),
        ('movimiento', 'Movimiento corporal'),
        ('sensorial', 'Anclaje sensorial'),
        ('cognitivo', 'Reencuadre cognitivo'),
        ('emocional', 'Regulación emocional'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructions = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    duration_minutes = models.IntegerField(default=5)
    image = models.ImageField(upload_to='regulacion/', blank=True, null=True)
    order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f'[{self.category}] {self.title}'
