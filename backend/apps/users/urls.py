from django.urls import path
from .views import CitizenCreateView

urlpatterns = [
    path('register/', CitizenCreateView.as_view(), name='citizen-register'),
]
