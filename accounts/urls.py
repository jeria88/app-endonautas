from django.contrib.auth import views as auth_views
from django.urls import include, path

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
    path('adios/', views.logout_done, name='logout_done'),
    path('eliminar-cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('r/<str:code>/', views.referral_redirect, name='referral_redirect'),

    # Password reset (Django built-in)
    path('recuperar/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/email/password_reset.txt',
        subject_template_name='accounts/email/password_reset_subject.txt',
    ), name='password_reset'),
    path('recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
    ), name='password_reset_done'),
    path('recuperar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
    ), name='password_reset_confirm'),
    path('recuperar/listo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html',
    ), name='password_reset_complete'),

    # OAuth (allauth)
    path('oauth/', include('allauth.urls')),
]
