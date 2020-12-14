"""Database Comments module"""
from django.db import models

class Notes(models.Model):
    """Database Comments model"""
    workflow = models.ForeignKey("Workflows", on_delete=models.CASCADE)
    user = models.ForeignKey("Users", on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    
