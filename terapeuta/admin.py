from django.contrib import admin
from .models import MarcoEvaluacion, TecnicaEvaluacion, Consulta, DiagnosticoPropuesto

admin.site.register(MarcoEvaluacion)
admin.site.register(TecnicaEvaluacion)
admin.site.register(Consulta)
admin.site.register(DiagnosticoPropuesto)
