from django.urls import path

from . import views

urlpatterns = [
    path('', views.birth_home, name='birth_home'),
    path('datos/', views.birth_datos, name='birth_datos'),
    path('astral/', views.birth_astral, name='birth_astral'),
    path('hd/', views.birth_hd, name='birth_hd'),
    path('saju/', views.birth_saju, name='birth_saju'),
]
