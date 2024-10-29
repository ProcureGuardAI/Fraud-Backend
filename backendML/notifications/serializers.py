# serializers.py
from rest_framework import serializers # type: ignore
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'transaction', 'message', 'notification_type', 'priority', 'is_read', 'created_at', 'updated_at']
