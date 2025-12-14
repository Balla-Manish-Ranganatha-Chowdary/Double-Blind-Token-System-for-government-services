from rest_framework import serializers
from .models import Citizen

class CitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ['id', 'name', 'age', 'address', 'aadhaar', 'created_at']
        read_only_fields = ['id', 'created_at']
