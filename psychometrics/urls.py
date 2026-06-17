from django.urls import path

from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('mis-resultados/', views.my_results, name='my_results'),
    path('mapa-interior/', views.mapa_interior, name='mapa_interior'),
    path('resultado/<int:pk>/', views.test_result, name='test_result'),
    path('resultado/<int:pk>/pdf/', views.test_result_pdf, name='test_result_pdf'),
    path('resultado/<int:pk>/compartir/', views.test_result_share, name='test_result_share'),
    path('mis-resultados/reponer/', views.reponer_resultados, name='reponer_resultados'),
    path('<slug:slug>/', views.test_detail, name='test_detail'),
    path('<slug:slug>/responder/', views.test_take, name='test_take'),
]
