from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MarcoEvaluacion(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    framework_code = models.CharField(max_length=10, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre


class TecnicaEvaluacion(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    marco = models.ForeignKey(MarcoEvaluacion, on_delete=models.CASCADE, related_name="tecnicas")
    codigo_interno = models.CharField(max_length=20, unique=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["marco__orden", "orden", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.marco.nombre})"


class Consulta(models.Model):
    MODO_CHOICES = [("autoconsulta", "Autoconsulta"), ("terapeuta", "Terapeuta")]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consultas_terapeuta",
        null=True, blank=True,
    )
    perfil_cliente = models.ForeignKey(
        'practitioners.TemporaryProfile',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='consultas',
    )
    modo = models.CharField(max_length=20, choices=MODO_CHOICES, default="autoconsulta")
    nombre_paciente = models.CharField(max_length=200, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(150)])
    ocupacion = models.CharField(max_length=200, blank=True)
    motivo = models.TextField(default="")
    intensidad = models.IntegerField(null=True, blank=True)
    duracion = models.CharField(max_length=20, blank=True,
        choices=[("agudo", "Agudo (<2 semanas)"), ("subagudo", "Subagudo (2-6 semanas)"), ("cronico", "Crónico (>6 semanas)")])
    medicamentos_actuales = models.TextField(blank=True)
    senales_alarma = models.BooleanField(default=False)
    prioridad_sintoma = models.TextField(blank=True)
    marcos_recomendados = models.JSONField(default=list, blank=True)
    # Rediseño anamnesis por signos + motor de ejes (Fase 1)
    sistemas_afectados = models.JSONField(default=list, blank=True)   # ["piel", ...] del triaje
    signos = models.JSONField(default=dict, blank=True)               # {"G01": "friolento", "P03": ["calor"], ...}
    ejes_resultado = models.JSONField(default=dict, blank=True)       # ejes acumulados (debug/persistencia)
    formula_mtc = models.JSONField(default=dict, blank=True)          # fórmula compositiva sintetizada
    diagnostico_final = models.TextField(blank=True)
    propuesta_terapeutica = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    paso_actual = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Consulta #{self.id} — {self.nombre_paciente or 'Sin nombre'}"


class SeleccionTecnica(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="selecciones")
    tecnica = models.ForeignKey(TecnicaEvaluacion, on_delete=models.CASCADE, related_name="selecciones")
    fue_recomendada_por_sistema = models.BooleanField(default=False)

    class Meta:
        unique_together = ["consulta", "tecnica"]


class PreguntaRespuesta(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="preguntas_respuestas")
    pregunta = models.TextField()
    respuesta = models.TextField(blank=True)
    tecnica_asociada = models.ForeignKey(TecnicaEvaluacion, on_delete=models.SET_NULL, null=True, blank=True, related_name="preguntas")
    pregunta_id = models.CharField(max_length=10, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]


class DiagnosticoPropuesto(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="diagnosticos")
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField(blank=True)
    marco_asociado = models.ForeignKey(MarcoEvaluacion, on_delete=models.SET_NULL, null=True, blank=True, related_name="diagnosticos")
    tecnica_asociada = models.ForeignKey(TecnicaEvaluacion, on_delete=models.SET_NULL, null=True, blank=True, related_name="diagnosticos")
    etiologia = models.TextField(blank=True)
    mecanismo = models.TextField(blank=True)
    patron_diagnostico = models.TextField(blank=True)
    protocolo_indicado = models.TextField(blank=True)
    contraindicaciones = models.TextField(blank=True)
    integracion = models.TextField(blank=True)
    fue_confirmado_por_usuario = models.BooleanField(default=False)
    diagnostico_id = models.CharField(max_length=10, blank=True)
    # Motor de diferenciación (Fase 1): puntaje y evidencia estructurada
    puntaje = models.FloatField(null=True, blank=True)
    confianza = models.FloatField(null=True, blank=True)
    evidencia = models.JSONField(default=dict, blank=True)  # {"a_favor": [...], "en_contra": [...], "justificacion_ia": ""}
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return self.titulo


class SintomaConfirmado(models.Model):
    diagnostico = models.ForeignKey(DiagnosticoPropuesto, on_delete=models.CASCADE, related_name="sintomas")
    sintoma_texto = models.CharField(max_length=200)
    presente = models.BooleanField(default=True)
