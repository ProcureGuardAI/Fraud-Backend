from django.db import models
from users.models import User


class Contract(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Flagged', 'Flagged'),
    ]
    

    title = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} (Status: {self.status})"
    
    def update_fraud_score(self, score):
        self.fraud_score = score
        self.is_flagged = score > 0.5  # Example threshold
        self.status = 'Flagged' if self.is_flagged else self.status
        self.save()
        
    def __str__(self):
        return f"Report for {self.email} at {self.created_at}"