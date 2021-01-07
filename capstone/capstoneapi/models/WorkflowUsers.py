"""Database RareUser module"""
from django.db import models
from django.contrib.auth.models import User

class WorkflowUsers(models.Model):
    """Database RareUser Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"