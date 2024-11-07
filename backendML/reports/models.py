from django.db import models
from users.models import User

<<<<<<< HEAD
class Contract(models.Model):
=======
class Report(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Flagged', 'Flagged'),
    ]
    
>>>>>>> origin/main
    title = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=50, unique=True)
    fraud_score = models.FloatField(null=True, blank=True)
    is_flagged = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.title} (Status: {self.status})"
    
    def update_fraud_score(self, score):
        self.fraud_score = score
        self.is_flagged = score > 0.5  # Example threshold
        self.status = 'Flagged' if self.is_flagged else self.status
        self.save()

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']
=======

    def __str__(self):
        return f"Report for {self.email} at {self.created_at}"
>>>>>>> e2547b448a2294b3b8149896b509cae05fa862af
