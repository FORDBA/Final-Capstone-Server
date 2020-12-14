"""Database Comments module"""
from django.db import models

class Workflows(models.Model):
    """Database Comments model"""
    due_date = models.DateField()
    completion_date = models.DateField()
    preparer = models.ForeignKey("Users", on_delete=models.SET_NULL)
    reviewer = models.ForeignKey("Users", on_delete=models.SET_NULL)
    processor = models.ForeignKey("Users", on_delete=models.SET_NULL)    
    status = models.ForeignKey("Statuses", on_delete=models.SET_NULL)
    state = models.ForeignKey("States", on_delete=models.SET_NULL)
    company = models.ForeignKey("Companies", on_delete=models.SET_NULL)
    
    
