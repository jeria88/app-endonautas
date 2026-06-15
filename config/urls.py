from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('tokens/', include('tokens.urls')),
    path('tests/', include('psychometrics.urls')),
    path('espejo/', include('mirror.urls')),
    path('nacimiento/', include('birth.urls')),
    path('comunidad/', include('community.urls')),
    path('practicantes/', include('practitioners.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
