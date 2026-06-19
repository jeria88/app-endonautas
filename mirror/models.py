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
    meta = models.JSONField(default=dict, blank=True)
    fecha = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} [{self.entry_type}] {self.fecha}'


class EjercicioRegulacion(models.Model):
    CATEGORY_CHOICES = [
        ('aliento',    'Aliento'),      # Respiración
        ('integracion','Integración'),  # Movimiento/Brain Gym
        ('resonancia', 'Resonancia'),   # Sonido/vibración
        ('espectro',   'Espectro'),     # Color y luz
        ('campo',      'Campo'),        # Contacto energético
        ('presencia',  'Presencia'),    # Consciencia e intención
    ]
    UI_MODE_CHOICES = [
        ('respiracion',  'Timer de respiración guiada'),
        ('pasos',        'Secuencia de pasos'),
        ('vocal',        'Guía vocal'),
        ('visualizacion','Visualización guiada'),
        ('reflexion',    'Reflexión libre'),
    ]

    title             = models.CharField(max_length=200)
    subtitle          = models.CharField(max_length=300, blank=True)
    description       = models.TextField(blank=True)
    instructions      = models.TextField()
    category          = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    ui_mode           = models.CharField(max_length=20, choices=UI_MODE_CHOICES, default='pasos')
    duration_minutes  = models.IntegerField(default=5)
    phases            = models.JSONField(default=list, blank=True)   # para ui_mode='respiracion'
    steps             = models.JSONField(default=list, blank=True)   # para ui_mode='pasos'/'vocal'
    emotional_targets = models.JSONField(default=list, blank=True)   # ['ansiedad','ira',...]
    body_zones        = models.JSONField(default=list, blank=True)   # ['mandibula','plexo',...]
    precaution        = models.CharField(max_length=400, blank=True)
    image             = models.ImageField(upload_to='regulacion/', blank=True, null=True)
    order             = models.IntegerField(default=0)
    active            = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order', 'title']

    def __str__(self):
        return f'[{self.category}] {self.title}'

    def as_json(self):
        return {
            'id': self.pk,
            'title': self.title,
            'subtitle': self.subtitle,
            'description': self.description,
            'instructions': self.instructions,
            'category': self.category,
            'ui_mode': self.ui_mode,
            'duration_minutes': self.duration_minutes,
            'phases': self.phases,
            'steps': self.steps,
            'emotional_targets': self.emotional_targets,
            'body_zones': self.body_zones,
            'precaution': self.precaution,
        }


class CategoriaNecesidad(models.Model):
    TIPO_CHOICES = [('cotidiano', 'Cotidiano'), ('crisis', 'Crisis')]
    nombre = models.CharField(max_length=100)
    slug   = models.SlugField(unique=True)
    tipo   = models.CharField(max_length=20, choices=TIPO_CHOICES)
    orden  = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.nombre


class MomentoRegulacion(models.Model):
    TIPO_CHOICES = [('cotidiano', 'Cotidiano'), ('crisis', 'Crisis')]
    nombre      = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True)
    tagline     = models.CharField(max_length=300, blank=True)
    image_key   = models.CharField(max_length=100, blank=True)  # slug para imagen futura
    duracion_min= models.PositiveSmallIntegerField(default=5)
    tipo        = models.CharField(max_length=20, choices=TIPO_CHOICES)
    categorias  = models.ManyToManyField(CategoriaNecesidad, blank=True, related_name='momentos')
    ejercicios  = models.ManyToManyField(EjercicioRegulacion, through='MomentoEjercicio', blank=True)
    orden       = models.PositiveSmallIntegerField(default=0)
    activo      = models.BooleanField(default=True)

    class Meta:
        ordering = ['tipo', 'orden']

    def __str__(self):
        return self.nombre

    def as_json(self):
        ejercicios_ordenados = [
            me.ejercicio.as_json()
            for me in self.momentoejercicio_set.select_related('ejercicio').order_by('orden')
        ]
        return {
            'id': self.pk,
            'nombre': self.nombre,
            'slug': self.slug,
            'tagline': self.tagline,
            'image_key': self.image_key,
            'duracion_min': self.duracion_min,
            'tipo': self.tipo,
            'categorias': list(self.categorias.values_list('slug', flat=True)),
            'ejercicios': ejercicios_ordenados,
        }


class MomentoEjercicio(models.Model):
    momento   = models.ForeignKey(MomentoRegulacion, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(EjercicioRegulacion, on_delete=models.CASCADE)
    orden     = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['orden']
        unique_together = [('momento', 'ejercicio')]
