from django.urls import path

from . import views

urlpatterns = [
    path('balance/', views.balance, name='tokens_balance'),
    path('historial/', views.historial, name='tokens_historial'),
]
