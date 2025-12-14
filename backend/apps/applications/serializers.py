from rest_framework import serializers
from .models import Application, ApplicationFile

class ApplicationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationFile
        fields = ['id', 'file', 'is_redacted', 'uploaded_at']

class ApplicationSerializer(serializers.ModelSerializer):
    files = ApplicationFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'token_te1', 'service_category', 'status', 'created_at', 'files']
        read_only_fields = ['id', 'token_te1', 'service_category', 'status', 'created_at']

class ApplicationCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    age = serializers.IntegerField()
    address = serializers.CharField()
    aadhaar = serializers.CharField(max_length=12)
    files = serializers.ListField(child=serializers.FileField())

class OfficerApplicationSerializer(serializers.ModelSerializer):
    """Serializer for officer view - shows TE2 token, hides citizen info"""
    files = ApplicationFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'token_te2', 'service_category', 'status', 'created_at', 'files']
        read_only_fields = ['id', 'token_te2', 'service_category', 'status', 'created_at']

class ApplicationActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['APPROVE', 'REJECT'])
    remarks = serializers.CharField(required=False, allow_blank=True)
