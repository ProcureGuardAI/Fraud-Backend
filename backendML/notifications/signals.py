# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Transaction
from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer # type: ignore

@receiver(post_save, sender=Transaction)
def create_notification_on_suspicious_transaction(sender, instance, created, **kwargs):
    if created and instance.is_suspicious:
        message = f'Suspicious transaction detected: Amount {instance.amount} on {instance.transaction_date}.'
        priority = 'high'
        notification_type = 'suspicious_transaction'

        Notification.objects.create(
            user=instance.user,
            transaction=instance,
            message=message,
            notification_type=notification_type,
            priority=priority
        )

@receiver(post_save, sender=Notification)
def send_real_time_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.user.id}',  # Send to the specific user
            {
                'type': 'send_notification',
                'message': instance.message,
                'notification_type': instance.notification_type,
                'priority': instance.priority,
                'created_at': str(instance.created_at),
            }
        )
