"""Database Comments module"""
from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    """Database Comments model"""
    workflow = models.ForeignKey("Workflows", on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    
