from django.db import models
from users.models import User

class Report(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Flagged', 'Flagged'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)
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
