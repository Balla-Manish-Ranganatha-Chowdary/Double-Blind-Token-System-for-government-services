from rest_framework import serializers
from .models import Officer

class OfficerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Officer
        fields = ['id', 'username', 'email', 'hierarchy_level', 'department', 'workload_count', 'is_active']

class OfficerCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    department = serializers.CharField(max_length=100)
    hierarchy_level = serializers.IntegerField(min_value=1, max_value=10)
