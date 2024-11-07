from django.db import models
from users.models import User
from core.models import CoreModel
# Create your models here.

class Contract(models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.email} at {self.created_at}"
