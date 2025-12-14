from django.contrib import admin
from .models import Officer

@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'hierarchy_level', 'workload_count', 'is_active']
    list_filter = ['department', 'hierarchy_level', 'is_active']
    search_fields = ['user__username', 'department']
