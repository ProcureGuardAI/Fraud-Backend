from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report
from notifications.models import Notification

@receiver(post_save, sender=Report)
def report_status_change(sender, instance, created, **kwargs):
    print(f"Signal triggered for report: {instance.title}, created: {created}, status: {instance.status}")  # Debugging: Print signal trigger
    if not created and instance.status == 'Resolved':
        print(f"Creating notification for report: {instance.title}")  # Debugging: Print when creating notification
        Notification.objects.create(
            user=instance.created_by,
            message=f"Report '{instance.title}' has been resolved.",
            is_read=False
        )