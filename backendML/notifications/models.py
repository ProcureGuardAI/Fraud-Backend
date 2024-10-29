# models.py
from django.db import models
from users.models import User
from core.models import Transaction

class Notification(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    TYPE_CHOICES = [
        ('suspicious_transaction', 'Suspicious Transaction'),
        ('account_anomaly', 'Account Anomaly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    notification_type = models.CharField(
    max_length=50, 
    choices=TYPE_CHOICES, 
    default='suspicious_transaction'  # Set a default choice here
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.get_priority_display()} priority: {self.message[:20]}'
