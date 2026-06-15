from django.urls import path

from . import views

urlpatterns = [
    path('', views.espejo_home, name='espejo_home'),
    path('chat/', views.chat_new, name='espejo_chat_new'),
    path('chat/<int:pk>/', views.chat_session, name='espejo_chat'),
    path('chat/<int:pk>/mensaje/', views.chat_message, name='espejo_message'),
    path('api/<int:pk>/', views.chat_session_api, name='espejo_session_api'),
]
