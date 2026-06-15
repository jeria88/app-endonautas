from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('perfil-social/', views.perfil_social, name='perfil_social'),
    path('perfil-social/<str:username>/', views.perfil_social, name='perfil_social_user'),
    path('onboarding/', views.onboarding, name='onboarding'),
]
