from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Application, ApplicationFile
from .serializers import ApplicationSerializer, ApplicationCreateSerializer, OfficerApplicationSerializer, ApplicationActionSerializer
from apps.users.models import Citizen
from apps.encryption.services import TokenEncryptionService
from apps.ai_services.classification import ServiceClassifier
from apps.ai_services.redaction import DocumentRedactor
from apps.officers.assignment import OfficerAssignmentAlgorithm

class ApplicationCreateView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ApplicationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Create citizen
        citizen = Citizen.objects.create(
            name=data['name'],
            age=data['age'],
            address=data['address'],
            aadhaar=data['aadhaar']
        )
        
        # Generate double-blind token
        token_service = TokenEncryptionService()
        original_token = token_service.generate_token()
        te1 = token_service.encrypt_te1(original_token)
        te2 = token_service.encrypt_te2(original_token)
        
        # Create application
        application = Application.objects.create(
            citizen=citizen,
            token_original=original_token,
            token_te1=te1,
            token_te2=te2
        )
        
        # Save files
        for file in data['files']:
            ApplicationFile.objects.create(
                application=application,
                file=file
            )
        
        # AI Redaction check FIRST (before classification)
        redactor = DocumentRedactor()
        for file in data['files']:
            has_pii = redactor.check_for_pii(file)
            if has_pii:
                application.status = 'REJECTED'
                application.save()
                return Response({
                    'error': 'Application rejected: Identity-bearing information detected in documents. Please remove all personal identifiers (name, Aadhaar, phone numbers) from uploaded documents.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # AI Classification
        classifier = ServiceClassifier()
        service_category = classifier.classify(data['files'][0] if data['files'] else None)
        application.service_category = service_category
        application.status = 'CLASSIFIED'
        application.save()
        
        # Auto-assign to officer based on workload
        assignment_algo = OfficerAssignmentAlgorithm()
        officer = assignment_algo.assign_officer(application, service_category)
        
        if officer:
            application.status = 'ASSIGNED'
        else:
            application.status = 'REDACTION_CLEARED'
        application.save()
        
        return Response({
            'token': te1,
            'message': 'Application submitted successfully',
            'application_id': application.id
        }, status=status.HTTP_201_CREATED)


class ApplicationStatusView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            application = Application.objects.get(token_te1=token)
            serializer = ApplicationSerializer(application)
            return Response(serializer.data)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)


class OfficerApplicationListView(APIView):
    """List applications assigned to logged-in officer"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            officer = request.user.officer
            applications = Application.objects.filter(
                assigned_officer=officer,
                status__in=['ASSIGNED', 'IN_REVIEW']
            )
            serializer = OfficerApplicationSerializer(applications, many=True)
            return Response(serializer.data)
        except:
            return Response({'error': 'Officer profile not found'}, status=status.HTTP_404_NOT_FOUND)


class ApplicationActionView(APIView):
    """Officer approves/rejects application"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, application_id):
        try:
            officer = request.user.officer
            application = Application.objects.get(id=application_id, assigned_officer=officer)
        except:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ApplicationActionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        action = serializer.validated_data['action']
        
        if action == 'APPROVE':
            # Check if needs next level approval
            assignment_algo = OfficerAssignmentAlgorithm()
            next_officer = assignment_algo.forward_to_next_level(application)
            
            if next_officer:
                application.status = 'FORWARDED'
                message = 'Application forwarded to next level'
            else:
                application.status = 'APPROVED'
                officer.workload_count -= 1
                officer.save()
                message = 'Application approved'
            
        elif action == 'REJECT':
            application.status = 'REJECTED'
            officer.workload_count -= 1
            officer.save()
            message = 'Application rejected'
        
        application.save()
        
        return Response({
            'message': message,
            'status': application.status
        })
