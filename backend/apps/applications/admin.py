from django.contrib import admin
from .models import Application, ApplicationFile

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'service_category', 'status', 'assigned_officer', 'created_at']
    list_filter = ['status', 'service_category']
    search_fields = ['token_te1', 'token_te2']
    readonly_fields = ['token_original', 'token_te1', 'token_te2', 'created_at', 'updated_at']

@admin.register(ApplicationFile)
class ApplicationFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'application', 'is_redacted', 'uploaded_at']
    list_filter = ['is_redacted']
