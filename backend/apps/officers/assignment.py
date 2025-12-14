from .models import Officer
from .constants import SERVICE_TO_DEPARTMENT
from apps.applications.models import Application


class OfficerAssignmentAlgorithm:
    """Workload-based officer assignment with hierarchy support"""
    
    def assign_officer(self, application: Application, service_category: str = None):
        """Assign officer based on workload and hierarchy"""
        
        # Use service_category from parameter or application
        if not service_category:
            service_category = application.service_category
        
        # Get department from service category using constants
        department = self._get_department(service_category)
        
        # Get officers at hierarchy level 1 for this department
        officers = Officer.objects.filter(
            department=department,
            hierarchy_level=1,
            is_active=True
        ).order_by('workload_count')
        
        if not officers.exists():
            # Try GENERAL department as fallback
            officers = Officer.objects.filter(
                department='GENERAL',
                hierarchy_level=1,
                is_active=True
            ).order_by('workload_count')
            
            if not officers.exists():
                return None
        
        # Assign to officer with lowest workload
        selected_officer = officers.first()
        selected_officer.workload_count += 1
        selected_officer.save()
        
        application.assigned_officer = selected_officer
        application.status = 'ASSIGNED'
        application.save()
        
        return selected_officer
    
    def forward_to_next_level(self, application: Application):
        """Forward application to next hierarchy level"""
        current_officer = application.assigned_officer
        if not current_officer:
            return None
        
        next_level = current_officer.hierarchy_level + 1
        
        # Get officers at next level in same department
        officers = Officer.objects.filter(
            department=current_officer.department,
            hierarchy_level=next_level,
            is_active=True
        ).order_by('workload_count')
        
        if not officers.exists():
            # No higher level, application is complete
            return None
        
        # Decrease workload of current officer
        current_officer.workload_count -= 1
        current_officer.save()
        
        # Assign to next level officer
        next_officer = officers.first()
        next_officer.workload_count += 1
        next_officer.save()
        
        application.assigned_officer = next_officer
        application.status = 'FORWARDED'
        application.save()
        
        return next_officer
    
    def _get_department(self, service_category: str) -> str:
        """Map service category to department using constants"""
        return SERVICE_TO_DEPARTMENT.get(service_category, 'GENERAL')
