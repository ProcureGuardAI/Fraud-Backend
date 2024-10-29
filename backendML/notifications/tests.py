# notifications/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient # type: ignore
from .models import Notification

User = get_user_model()

class NotificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)

        # Create a sample notification
        self.notification = Notification.objects.create(
            user=self.user,
            message="Suspicious activity detected!",
            is_read=False,
        )

    def test_get_notifications(self):
        response = self.client.get('/api/notifications/notifications/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Suspicious activity detected!', response.data[0]['message'])

    def test_mark_notification_as_read(self):
        response = self.client.post(f'/api/notifications/notifications/{self.notification.id}/mark_as_read/')
        self.assertEqual(response.status_code, 200)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)