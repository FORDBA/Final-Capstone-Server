"""Database Comments module"""
from django.db import models
from django.contrib.auth.models import User

class Workflows(models.Model):
    """Database Comments model"""
    due_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    preparer = models.OneToOneField(User, related_name='user_preparer', on_delete=models.CASCADE)
    reviewer = models.OneToOneField(User, related_name='user_reviewer', on_delete=models.CASCADE)
    processor = models.OneToOneField(User, related_name='user_processor', on_delete=models.CASCADE)    
    status = models.ForeignKey("Statuses", on_delete=models.DO_NOTHING)
    state = models.ForeignKey("States", on_delete=models.DO_NOTHING)
    company = models.ForeignKey("Companies", on_delete=models.DO_NOTHING)
    
    
