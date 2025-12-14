from django.urls import path
from .views import (
    ApplicationCreateView, 
    ApplicationStatusView,
    OfficerApplicationListView,
    ApplicationActionView
)

urlpatterns = [
    path('submit/', ApplicationCreateView.as_view(), name='application-submit'),
    path('status/<str:token>/', ApplicationStatusView.as_view(), name='application-status'),
    path('officer/list/', OfficerApplicationListView.as_view(), name='officer-applications'),
    path('officer/action/<int:application_id>/', ApplicationActionView.as_view(), name='application-action'),
]
