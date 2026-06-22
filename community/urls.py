from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='community_feed'),
    path('publicar/', views.post_create, name='community_post_create'),
    path('post/<int:pk>/', views.post_detail, name='community_post_detail'),
    path('post/<int:pk>/reaccionar/', views.post_react, name='community_post_react'),
    path('compartir/', views.share_create, name='community_share'),
    path('foros/', views.foros, name='foros'),
    path('foros/<slug:slug>/', views.forum_detail, name='forum_detail'),
    path('foros/<slug:slug>/nuevo/', views.forum_post_create, name='forum_post_create'),
    path('foros/<slug:slug>/<int:pk>/', views.forum_post_detail, name='forum_post_detail'),
    path('mensajes/', views.mensajes, name='mensajes'),
]
