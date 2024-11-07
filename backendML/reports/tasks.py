from .models import Report
from notifications.models import Notification  # Import Notification from notifications app

def run_fraud_detection(report):
    # Mock-up fraud detection; replace with actual ML model prediction
    fraud_score = 0.8  # Hypothetical ML score
    report.fraud_score = fraud_score
    report.is_flagged = fraud_score > 0.7  # Flag if score > threshold
    report.status = 'Flagged' if report.is_flagged else report.status
    report.save()
    
    if report.is_flagged:
        # Send real-time alert to admin or related user
        Notification.objects.create(
            user=report.created_by,
            message=f"Transaction '{report.transaction_id}' flagged as suspicious!",
            is_read=False
        )
