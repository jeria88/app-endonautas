from django.urls import path

from . import views

urlpatterns = [
    path('', views.espejo_home, name='espejo_home'),
    path('chat/', views.chat_new, name='espejo_chat_new'),
    path('chat/<int:pk>/', views.chat_session, name='espejo_chat'),
    path('chat/<int:pk>/mensaje/', views.chat_message, name='espejo_message'),
    path('api/<int:pk>/', views.chat_session_api, name='espejo_session_api'),
    path('chat/<int:pk>/renombrar/', views.chat_session_rename, name='espejo_rename'),
    path('chat/<int:pk>/eliminar/', views.chat_session_delete, name='espejo_delete'),
    path('chat/<int:pk>/exportar/', views.chat_session_export, name='espejo_export'),
    # Bitácora
    path('bitacora/', views.bitacora_list, name='bitacora_list'),
    path('bitacora/nueva/', views.bitacora_create, name='bitacora_create'),
    path('bitacora/<int:pk>/editar/', views.bitacora_edit, name='bitacora_edit'),
    path('bitacora/<int:pk>/eliminar/', views.bitacora_delete, name='bitacora_delete'),
]
