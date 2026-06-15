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
    path('foros/', community_views.foros, name='foros'),
    path('mensajes/', community_views.mensajes, name='mensajes'),
    path('nacimiento/', include('birth.urls')),
    path('comunidad/', include('community.urls')),
    path('practicantes/', include('practitioners.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
