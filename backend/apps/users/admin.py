from django.contrib import admin
from .models import Citizen

@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'age', 'created_at']
    search_fields = ['name', 'aadhaar']
    readonly_fields = ['created_at']
