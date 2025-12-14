"""
Unit tests for officer management and assignment
"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Officer
from .assignment import OfficerAssignmentAlgorithm
from apps.applications.models import Application


class OfficerModelTests(TestCase):
    """Test Officer model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='officer1',
            password='officer123'
        )
    
    def test_create_officer(self):
        """Test creating an officer"""
        officer = Officer.objects.create(
            user=self.user,
            department='REVENUE',
            hierarchy_level=1,
            is_active=True
        )
        self.assertIsNotNone(officer.id)
        self.assertEqual(officer.department, 'REVENUE')
        self.assertEqual(officer.workload_count, 0)
    
    def test_officer_workload_increment(self):
        """Test incrementing officer workload"""
        officer = Officer.objects.create(
            user=self.user,
            department='REVENUE',
            hierarchy_level=1,
            is_active=True
        )
        
        initial_workload = officer.workload_count
        officer.workload_count += 1
        officer.save()
        
        self.assertEqual(officer.workload_count, initial_workload + 1)
    
    def test_officer_deactivation(self):
        """Test deactivating an officer"""
        officer = Officer.objects.create(
            user=self.user,
            department='REVENUE',
            hierarchy_level=1,
            is_active=True
        )
        
        officer.is_active = False
        officer.save()
        
        self.assertFalse(officer.is_active)


class OfficerAssignmentTests(TestCase):
    """Test officer assignment algorithm"""
    
    def setUp(self):
        # Create multiple officers
        self.officers = []
        for i in range(3):
            user = User.objects.create_user(
                username=f'officer{i}',
                password='officer123'
            )
            officer = Officer.objects.create(
                user=user,
                department='REVENUE',
                hierarchy_level=1,
                is_active=True,
                workload_count=i  # Different workloads
            )
            self.officers.append(officer)
        
        self.algorithm = OfficerAssignmentAlgorithm()
    
    def test_assign_to_lowest_workload(self):
        """Test assignment to officer with lowest workload"""
        app = Application.objects.create(
            applicant_name="Test User",
            applicant_email="test@example.com",
            service_category="REVENUE",
            status="CLASSIFIED"
        )
        
        assigned_officer = self.algorithm.assign_officer(app)
        
        self.assertIsNotNone(assigned_officer)
        # Should assign to officer with workload_count = 0
        self.assertEqual(assigned_officer.workload_count, 0)
    
    def test_no_active_officers(self):
        """Test assignment when no active officers available"""
        # Deactivate all officers
        Officer.objects.all().update(is_active=False)
        
        app = Application.objects.create(
            applicant_name="Test User",
            applicant_email="test@example.com",
            service_category="REVENUE",
            status="CLASSIFIED"
        )
        
        assigned_officer = self.algorithm.assign_officer(app)
        self.assertIsNone(assigned_officer)
    
    def test_department_matching(self):
        """Test assignment matches department"""
        # Create officer in different department
        user = User.objects.create_user(
            username='officer_health',
            password='officer123'
        )
        health_officer = Officer.objects.create(
            user=user,
            department='HEALTH',
            hierarchy_level=1,
            is_active=True,
            workload_count=0
        )
        
        app = Application.objects.create(
            applicant_name="Test User",
            applicant_email="test@example.com",
            service_category="HEALTH",
            status="CLASSIFIED"
        )
        
        assigned_officer = self.algorithm.assign_officer(app)
        
        self.assertIsNotNone(assigned_officer)
        self.assertEqual(assigned_officer.department, 'HEALTH')
