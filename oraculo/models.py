import uuid
from django.db import models
from django.conf import settings


class CartaFractal(models.Model):
    TIPO_CARTA = [("arcano", "Arcano Mayor"), ("sefirot", "Sefirot")]
    numero = models.PositiveSmallIntegerField(unique=True)
    nombre_arcano = models.CharField(max_length=100)
    verbo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=TIPO_CARTA, default="arcano")
    descripcion_breve = models.TextField()
    descripcion_larga = models.TextField(blank=True)
    sefirot_nombre = models.CharField(max_length=50, blank=True)
    es_especial = models.BooleanField(default=False)

    class Meta:
        ordering = ["numero"]
        verbose_name = "Carta Fractal"
        verbose_name_plural = "Cartas Fractales"

    def __str__(self):
        return f"{self.numero}. {self.nombre_arcano} — {self.verbo}"


class SesionOraculo(models.Model):
    TIPO = [
        ("tarot", "Tarot Terapéutico"),
        ("iching", "I Ching"),
        ("fractal", "Oráculo Fractal"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sesiones_oraculo",
        null=True, blank=True,
    )
    tipo_oraculo = models.CharField(max_length=20, choices=TIPO)
    pregunta = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    guardada = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "Sesión de Oráculo"
        verbose_name_plural = "Sesiones de Oráculo"

    def __str__(self):
        return f"[{self.get_tipo_oraculo_display()}] {self.pregunta[:50]}"


class LecturaTarot(models.Model):
    sesion = models.OneToOneField(SesionOraculo, on_delete=models.CASCADE, related_name="lectura_tarot")
    tipo_tirada = models.CharField(max_length=20)
    cartas = models.JSONField(default=list)
    interpretacion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Lectura de Tarot"


class LecturaIChing(models.Model):
    sesion = models.OneToOneField(SesionOraculo, on_delete=models.CASCADE, related_name="lectura_iching")
    lineas = models.JSONField(default=list)
    hexagrama_primario_numero = models.PositiveIntegerField(null=True, blank=True)
    hexagrama_primario_nombre = models.CharField(max_length=100, blank=True)
    hexagrama_secundario_numero = models.PositiveIntegerField(null=True, blank=True)
    hexagrama_secundario_nombre = models.CharField(max_length=100, blank=True)
    interpretacion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Lectura I Ching"


class LecturaFractal(models.Model):
    sesion = models.OneToOneField(SesionOraculo, on_delete=models.CASCADE, related_name="lectura_fractal")
    carta = models.ForeignKey(CartaFractal, on_delete=models.SET_NULL, null=True, blank=True)
    invertida = models.BooleanField(default=False)
    interpretacion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Lectura Fractal"
