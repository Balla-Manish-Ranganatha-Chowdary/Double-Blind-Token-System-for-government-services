from django.urls import path
from .views import (
    OfficerListView,
    OfficerCreateView,
    OfficerUpdateView,
    OfficerDeleteView
)

urlpatterns = [
    path('', OfficerListView.as_view(), name='officer-list'),
    path('create/', OfficerCreateView.as_view(), name='officer-create'),
    path('update/<int:officer_id>/', OfficerUpdateView.as_view(), name='officer-update'),
    path('delete/<int:officer_id>/', OfficerDeleteView.as_view(), name='officer-delete'),
]
