from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from community import views as community_views
from config import wellknown
from mirror import views as mirror_views
from payments.views import planes_views
from reports import views as reports_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manifest.json', wellknown.manifest, name='manifest'),
    path('.well-known/assetlinks.json', wellknown.assetlinks, name='assetlinks'),
    path('', include('accounts.urls')),
    path('tokens/', include('tokens.urls')),
    path('tests/', include('psychometrics.urls')),
    path('espejo/', include('mirror.urls')),
    path('regulacion/', mirror_views.regulacion, name='regulacion'),
    path('regulacion/api/', mirror_views.regulacion_api, name='regulacion_api'),
    path('regulacion/completado/', mirror_views.regulacion_completado, name='regulacion_completado'),
    path('suenos/', mirror_views.suenos_list, name='suenos_list'),
    path('suenos/nuevo/', mirror_views.sueno_create, name='sueno_create'),
    path('suenos/<int:pk>/', mirror_views.sueno_detail, name='sueno_detail'),
    path('bitacora/', mirror_views.bitacora_list, name='bitacora_list'),
    path('bitacora/nueva/', mirror_views.bitacora_create, name='bitacora_create'),
    path('bitacora/<int:pk>/editar/', mirror_views.bitacora_edit, name='bitacora_edit'),
    path('bitacora/<int:pk>/eliminar/', mirror_views.bitacora_delete, name='bitacora_delete'),
    path('foros/', community_views.foros, name='foros'),
    path('mensajes/', community_views.mensajes, name='mensajes'),
    path('nacimiento/', include('birth.urls')),
    path('comunidad/', include('community.urls')),
    path('practicantes/', include('practitioners.urls')),
    path('oraculo/', include('oraculo.urls', namespace='oraculo')),
    path('terapeuta/', include('terapeuta.urls', namespace='terapeuta')),
    path('planes/', planes_views.planes, name='planes'),
    path('pago/', include('payments.urls')),
    path('terminos/', TemplateView.as_view(template_name='legal/terminos.html'), name='terminos'),
    path('api/reports/', include('reports.urls')),
    path('api/bug-report/', reports_views.bug_report, name='bug_report'),
    path('api/bug-report/captura/<int:pk>/', reports_views.bug_screenshot, name='bug_screenshot'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
