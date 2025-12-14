from django.db import models
from apps.users.models import Citizen
from apps.officers.models import Officer

class Application(models.Model):
    """Application model with double-blind token"""
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('CLASSIFIED', 'Classified'),
        ('REDACTION_CLEARED', 'Redaction Cleared'),
        ('ASSIGNED', 'Assigned'),
        ('IN_REVIEW', 'In Review'),
        ('FORWARDED', 'Forwarded to Next Level'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    token_original = models.CharField(max_length=255, unique=True)
    token_te1 = models.TextField()
    token_te2 = models.TextField()
    service_category = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    assigned_officer = models.ForeignKey(Officer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'applications'
    
    def __str__(self):
        return f"Application {self.id} - {self.status}"


class ApplicationFile(models.Model):
    """Uploaded files for applications"""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='applications/')
    is_redacted = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'application_files'
