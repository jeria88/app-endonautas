from django.urls import path
from . import views

app_name = "oraculo"

urlpatterns = [
    path("", views.hub, name="hub"),
    path("tarot/", views.tarot_view, name="tarot"),
    path("iching/", views.iching_view, name="iching"),
    path("fractal/", views.fractal_view, name="fractal"),
    path("api/tarot/", views.tarot_api, name="api_tarot"),
    path("api/iching/", views.iching_api, name="api_iching"),
    path("api/fractal/", views.fractal_api, name="api_fractal"),
]
