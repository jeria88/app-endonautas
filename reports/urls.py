from django.urls import path
from reports import views

urlpatterns = [
    path('weekly/latest/', views.weekly_latest, name='reports_weekly_latest'),
]
