from django.urls import path

from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('<slug:slug>/', views.test_detail, name='test_detail'),
    path('<slug:slug>/responder/', views.test_take, name='test_take'),
    path('resultado/<int:pk>/', views.test_result, name='test_result'),
    path('mis-resultados/', views.my_results, name='my_results'),
]
