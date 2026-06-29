from django.contrib import admin
from reports.models import KPISnapshot


@admin.register(KPISnapshot)
class KPISnapshotAdmin(admin.ModelAdmin):
    list_display = ('week_start', 'week_number', 'year', 'escenario', 'registros_nuevos', 'navegantes_total', 'mrr_estimado_usd', 'retencion_d30_pct', 'serpbear_posicion_avg', 'posts_publicados_semana', 'created_at')
    list_filter = ('escenario', 'year')
    readonly_fields = ('md_snapshot', 'created_at', 'alertas', 'decision_sugerida', 'fuentes_top', 'serpbear_keywords_top3')
    ordering = ('-week_start',)
