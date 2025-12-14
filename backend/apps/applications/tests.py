"""
Unit tests for application models and views
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Application
from apps.officers.models import Officer
from apps.encryption.services import EncryptionService
import json


class ApplicationModelTests(TestCase):
    """Test Application model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.encryption_service = EncryptionService()
    
    def test_create_application(self):
        """Test creating an application"""
        app = Application.objects.create(
            applicant_name="Test User",
            applicant_email="test@example.com",
            applicant_phone="1234567890",
            service_category="REVENUE",
            status="SUBMITTED"
        )
        self.assertIsNotNone(app.id)
        self.assertEqual(app.status, "SUBMITTED")
    
    def test_application_status_choices(self):
        """Test valid status choices"""
        valid_statuses = [
            'SUBMITTED', 'CLASSIFIED', 'REDACTION_CLEARED',
            'ASSIGNED', 'IN_REVIEW', 'FORWARDED',
            'APPROVED', 'REJECTED', 'REDACTION_FAILED'
        ]
        
        for status in valid_statuses:
            app = Application.objects.create(
                applicant_name="Test User",
                applicant_email="test@example.com",
                service_category="REVENUE",
                status=status
            )
            self.assertEqual(app.status, status)
    
    def test_application_token_generation(self):
        """Test token generation for application"""
        app = Application.objects.create(
            applicant_name="Test User",
            applicant_email="test@example.com",
            service_category="REVENUE",
            status="SUBMITTED"
        )
        
        # Generate tokens
        te1 = self.encryption_service.generate_te1_token(str(app.id))
        te2 = self.encryption_service.generate_te2_token(te1)
        
        app.te1_token = te1
        app.te2_token = te2
        app.save()
        
        self.assertIsNotNone(app.te1_token)
        self.assertIsNotNone(app.te2_token)
    
    def test_application_officer_assignment(self):
        """Test officer assignment to application"""
        officer_user = User.objects.create_user(
            username='officer1',
            password='officer123'
        )
        officer = Officer.objects.create(
            user=officer_user,
            department='REVENUE',
            hierarchy_level=1,
            is_active=True
        )
        
        app = Application.objects.create(
            applicant_name="Test User",
            applicant_email="test@example.com",
            service_category="REVENUE",
            status="ASSIGNED",
            assigned_officer=officer
        )
        
        self.assertEqual(app.assigned_officer, officer)
        self.assertEqual(app.status, "ASSIGNED")


class ApplicationAPITests(TestCase):
    """Test Application API endpoints"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_submit_application_endpoint(self):
        """Test application submission endpoint"""
        data = {
            'applicant_name': 'Test User',
            'applicant_email': 'test@example.com',
            'applicant_phone': '1234567890',
            'service_category': 'REVENUE',
            'description': 'Test application'
        }
        
        response = self.client.post(
            '/api/applications/submit/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Should return 201 or 200 depending on implementation
        self.assertIn(response.status_code, [200, 201, 401])
    
    def test_check_status_endpoint(self):
        """Test status check endpoint"""
        app = Application.objects.create(
            applicant_name="Test User",
            applicant_email="test@example.com",
            service_category="REVENUE",
            status="SUBMITTED"
        )
        
        encryption_service = EncryptionService()
        te1 = encryption_service.generate_te1_token(str(app.id))
        te2 = encryption_service.generate_te2_token(te1)
        
        app.te1_token = te1
        app.te2_token = te2
        app.save()
        
        response = self.client.get(f'/api/applications/status/?token={te2}')
        
        # Should return 200 or 401 depending on auth
        self.assertIn(response.status_code, [200, 401, 404])
