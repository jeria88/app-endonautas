from django.contrib import admin
from django.utils.html import format_html

from reports.models import BugReport, BugScreenshot, KPISnapshot


@admin.register(KPISnapshot)
class KPISnapshotAdmin(admin.ModelAdmin):
    list_display = ('week_start', 'week_number', 'year', 'escenario', 'registros_nuevos', 'navegantes_total', 'mrr_estimado_usd', 'retencion_d30_pct', 'serpbear_posicion_avg', 'posts_publicados_semana', 'created_at')
    list_filter = ('escenario', 'year')
    readonly_fields = ('md_snapshot', 'created_at', 'alertas', 'decision_sugerida', 'fuentes_top', 'serpbear_keywords_top3')
    ordering = ('-week_start',)


class BugScreenshotInline(admin.TabularInline):
    model = BugScreenshot
    extra = 0
    readonly_fields = ['preview']
    fields = ['preview']

    def preview(self, obj):
        if not obj.pk:
            return '—'
        return format_html(
            '<a href="/api/bug-report/captura/{}/" target="_blank">'
            '<img src="/api/bug-report/captura/{}/" style="max-height:220px"></a>',
            obj.pk, obj.pk)


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'estado', 'descripcion', 'user', 'pagina', 'creado']
    list_filter = ['estado', 'creado']
    list_editable = ['estado']
    search_fields = ['descripcion', 'user__email']
    readonly_fields = ['user', 'descripcion', 'pagina', 'user_agent', 'creado']
    inlines = [BugScreenshotInline]
