from django.db import models
from django.contrib.auth.models import User

class Officer(models.Model):
    """Officer model with hierarchy support"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hierarchy_level = models.IntegerField(default=1)
    department = models.CharField(max_length=100)
    workload_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'officers'
    
    def __str__(self):
        return f"{self.user.username} - Level {self.hierarchy_level}"
