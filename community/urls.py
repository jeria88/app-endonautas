from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='community_feed'),
    path('publicar/', views.post_create, name='community_post_create'),
    path('post/<int:pk>/', views.post_detail, name='community_post_detail'),
    path('post/<int:pk>/reaccionar/', views.post_react, name='community_post_react'),
    path('foros/', views.foros, name='foros'),
    path('mensajes/', views.mensajes, name='mensajes'),
]
