from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from community import views as community_views
from mirror import views as mirror_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('tokens/', include('tokens.urls')),
    path('tests/', include('psychometrics.urls')),
    path('espejo/', include('mirror.urls')),
    path('regulacion/', mirror_views.regulacion, name='regulacion'),
    path('suenos/', mirror_views.suenos_list, name='suenos_list'),
    path('suenos/nuevo/', mirror_views.sueno_create, name='sueno_create'),
    path('suenos/<int:pk>/', mirror_views.sueno_detail, name='sueno_detail'),
    path('bitacora/', mirror_views.bitacora_list, name='bitacora_list'),
    path('bitacora/nueva/', mirror_views.bitacora_create, name='bitacora_create'),
    path('bitacora/<int:pk>/eliminar/', mirror_views.bitacora_delete, name='bitacora_delete'),
    path('nauminto/', mirror_views.nauminto_list, name='nauminto_list'),
    path('nauminto/nuevo/', mirror_views.nauminto_create, name='nauminto_create'),
    path('nauminto/<int:pk>/', mirror_views.nauminto_detail, name='nauminto_detail'),
    path('foros/', community_views.foros, name='foros'),
    path('mensajes/', community_views.mensajes, name='mensajes'),
    path('nacimiento/', include('birth.urls')),
    path('comunidad/', include('community.urls')),
    path('practicantes/', include('practitioners.urls')),
    path('oraculo/', include('oraculo.urls', namespace='oraculo')),
    path('terapeuta/', include('terapeuta.urls', namespace='terapeuta')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
