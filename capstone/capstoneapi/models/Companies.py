"""Database Tag module"""
from django.db import models

class Companies(models.Model):
    """Database Tag model"""
    name = models.CharField(max_length=50)