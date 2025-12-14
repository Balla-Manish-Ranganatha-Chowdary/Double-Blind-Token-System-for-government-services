from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.get_dashboard_stats, name='dashboard-stats'),
    path('health/', views.health_check, name='health-check'),
]
