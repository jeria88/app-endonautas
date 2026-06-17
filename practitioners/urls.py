from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='practitioners_dashboard'),
    path('cliente/nuevo/', views.client_create, name='practitioners_client_create'),
    path('cliente/<int:pk>/', views.client_detail, name='practitioners_client_detail'),
    path('cliente/<int:pk>/nota/', views.session_note_create, name='practitioners_note_create'),
    path('agenda/', views.agenda, name='practitioners_agenda'),
    path('agenda/nueva/', views.session_create, name='practitioners_session_create'),
    path('disponibilidad/', views.availability, name='practitioners_availability'),
    path('cliente/<int:pk>/asignar-test/', views.assign_test, name='practitioners_assign_test'),
    path('fichas/', views.fichas_list, name='practitioners_fichas'),
    path('fichas/nueva/<int:profile_pk>/', views.ficha_create, name='practitioners_ficha_create'),
    path('invitar/<uuid:code>/', views.claim_profile, name='practitioners_claim'),
]
