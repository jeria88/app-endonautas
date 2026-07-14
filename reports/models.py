from django.db import models


class KPISnapshot(models.Model):
    week_start = models.DateField(db_index=True, unique=True)
    week_number = models.IntegerField()
    year = models.IntegerField()

    # KPIs Django ORM
    registros_nuevos = models.IntegerField(default=0)
    activacion_pct = models.FloatField(default=0)
    retencion_d7_pct = models.FloatField(default=0)
    retencion_d30_pct = models.FloatField(default=0)
    sesiones_espejo_avg = models.FloatField(default=0)
    navegantes_total = models.IntegerField(default=0)
    navegantes_nuevos_semana = models.IntegerField(default=0)
    mrr_estimado_usd = models.FloatField(default=0)

    # KPIs Listmonk
    email_open_rate_pct = models.FloatField(default=0)
    email_ctr_pct = models.FloatField(default=0)
    suscriptores_total = models.IntegerField(default=0)

    # KPIs Umami
    visitas_landing = models.IntegerField(default=0)
    visitas_unicas = models.IntegerField(default=0)
    fuentes_top = models.JSONField(default=dict)

    # SEO — SerpBear
    serpbear_keywords_top3 = models.JSONField(default=dict)
    serpbear_posicion_avg = models.FloatField(default=0)
    serpbear_subiendo = models.IntegerField(default=0)

    # RRSS — tráfico desde Umami por red
    trafico_instagram = models.IntegerField(default=0)
    trafico_tiktok = models.IntegerField(default=0)
    trafico_linkedin = models.IntegerField(default=0)

    # RRSS — manual o scraping automático
    posts_publicados_semana = models.IntegerField(default=0)
    instagram_seguidores = models.IntegerField(default=0)
    instagram_alcance = models.IntegerField(default=0)
    tiktok_seguidores = models.IntegerField(default=0)
    youtube_seguidores = models.IntegerField(default=0)
    facebook_seguidores = models.IntegerField(default=0)
    linkedin_seguidores = models.IntegerField(default=0)
    top_content = models.JSONField(default=dict)

    # Clasificación escenario
    escenario = models.CharField(
        max_length=10,
        choices=[('verde', 'Verde'), ('amarillo', 'Amarillo'), ('rojo', 'Rojo')],
        default='rojo',
    )
    alertas = models.JSONField(default=list)
    decision_sugerida = models.TextField(blank=True)

    md_snapshot = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-week_start']

    def __str__(self):
        return f"KPI {self.year}-W{self.week_number:02d} [{self.escenario}]"


class BugReport(models.Model):
    ESTADOS = [('nuevo', 'Nuevo'), ('revisado', 'Revisado'), ('resuelto', 'Resuelto')]
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bug_reports')
    descripcion = models.TextField()
    pagina = models.CharField(max_length=300, blank=True)
    user_agent = models.CharField(max_length=400, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='nuevo')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f"[{self.estado}] {self.descripcion[:50]}"


class BugScreenshot(models.Model):
    report = models.ForeignKey(BugReport, on_delete=models.CASCADE, related_name='capturas')
    imagen = models.BinaryField()
    content_type = models.CharField(max_length=60, default='image/png')
