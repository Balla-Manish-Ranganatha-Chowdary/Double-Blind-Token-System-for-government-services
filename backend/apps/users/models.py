from django.db import models
from django.contrib.auth.models import AbstractUser

class Citizen(models.Model):
    """Citizen user model with encrypted PII"""
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.TextField()
    aadhaar = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'citizens'
    
    def __str__(self):
        return f"Citizen {self.id}"
