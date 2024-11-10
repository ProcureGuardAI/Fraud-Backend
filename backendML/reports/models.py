from django.db import models

class Reports(models.Model):
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Flagged', 'Flagged'),
    ]
    

    title = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    prediction = models.IntegerField(null=True, blank=True)
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
        
class Meta:
    db_table = "reports_reports" 