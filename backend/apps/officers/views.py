from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from .models import Officer
from .serializers import OfficerSerializer, OfficerCreateSerializer

class OfficerListView(generics.ListAPIView):
    queryset = Officer.objects.filter(is_active=True)
    serializer_class = OfficerSerializer
    permission_classes = [permissions.IsAdminUser]


class OfficerCreateView(APIView):
    """Admin creates new officer"""
    permission_classes = [permissions.IsAdminUser]
    
    def post(self, request):
        serializer = OfficerCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Create user
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data.get('email', '')
        )
        
        # Create officer profile
        officer = Officer.objects.create(
            user=user,
            department=data['department'],
            hierarchy_level=data['hierarchy_level']
        )
        
        return Response({
            'message': 'Officer created successfully',
            'officer_id': officer.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)


class OfficerUpdateView(APIView):
    """Admin updates officer details"""
    permission_classes = [permissions.IsAdminUser]
    
    def patch(self, request, officer_id):
        try:
            officer = Officer.objects.get(id=officer_id)
        except Officer.DoesNotExist:
            return Response({'error': 'Officer not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update allowed fields
        if 'department' in request.data:
            officer.department = request.data['department']
        if 'hierarchy_level' in request.data:
            officer.hierarchy_level = request.data['hierarchy_level']
        if 'is_active' in request.data:
            officer.is_active = request.data['is_active']
        
        officer.save()
        
        serializer = OfficerSerializer(officer)
        return Response(serializer.data)


class OfficerDeleteView(APIView):
    """Admin deactivates officer"""
    permission_classes = [permissions.IsAdminUser]
    
    def delete(self, request, officer_id):
        try:
            officer = Officer.objects.get(id=officer_id)
            officer.is_active = False
            officer.save()
            return Response({'message': 'Officer deactivated successfully'})
        except Officer.DoesNotExist:
            return Response({'error': 'Officer not found'}, status=status.HTTP_404_NOT_FOUND)
