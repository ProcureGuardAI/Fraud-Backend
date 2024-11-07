from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient # type: ignore
from rest_framework import status # type: ignore
from django.urls import reverse
from .models import Report
from notifications.models import Notification
from .serializers import ReportSerializer
import json

User = get_user_model()

class ReportTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        
        # Authenticate as a regular user for basic tests
        self.client.force_authenticate(user=self.user)
        
        # Create sample reports
        self.report = Report.objects.create(
            title="Test Report",
            description="This is a test report.",
            created_by=self.user,
            transaction_id="txn123"
        )
        
    def test_create_report(self):
        """Test creating a report via the API."""
        data = {
            'title': 'New Report',
            'description': 'Details of the new report',
            'transaction_id': 'txn456',
            'created_by': self.user.id
        }
        response = self.client.post(reverse('report-list'), data=json.dumps(data), content_type='application/json')
        print(response.status_code)  # Debugging: Print the status code
        print(response.data)  # Debugging: Print the response data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if the report was created with correct details
        created_report = Report.objects.get(title="New Report")
        self.assertEqual(created_report.description, data['description'])
        self.assertEqual(created_report.created_by, self.user)

    def test_get_report_list(self):
        """Test retrieving a list of reports."""
        response = self.client.get(reverse('report-list'))
        print(response.status_code)  # Debugging: Print the status code
        print(response.data)  # Debugging: Print the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Validate that the report is in the list
        reports = Report.objects.filter(created_by=self.user)
        serializer = ReportSerializer(reports, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_update_report_status(self):
        """Test updating a report's status."""
        self.client.force_authenticate(user=self.admin)  # Only admin can update status
        
        # Flag the report first
        self.report.is_flagged = True
        self.report.save()
        
        data = {'status': 'Resolved'}
        response = self.client.patch(reverse('report-detail', args=[self.report.id]), data=json.dumps(data), content_type='application/json')
        print(response.status_code)  # Debugging: Print the status code
        print(response.data)  # Debugging: Print the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.report.refresh_from_db()
        self.assertEqual(self.report.status, 'Resolved')

    def test_run_fraud_detection(self):
        """Test fraud detection process on a report."""
        from .tasks import run_fraud_detection
        
        # Run fraud detection for the report
        run_fraud_detection(self.report)
        
        # Refresh the report to check updated fields
        self.report.refresh_from_db()
        self.assertEqual(self.report.is_flagged, True)
        self.assertEqual(self.report.status, 'Flagged')
        
    def test_notification_on_status_change(self):
        """Test notification creation when report status changes."""
        # Authenticate as admin to change status
        self.client.force_authenticate(user=self.admin)
        
        # Flag the report first
        self.report.is_flagged = True
        self.report.save()

        data = {'status': 'Resolved'}
        response = self.client.patch(reverse('report-detail', args=[self.report.id]), data=json.dumps(data), content_type='application/json')
        print(response.status_code)  # Debugging: Print the status code
        print(response.data)  # Debugging: Print the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if a notification was created
        notification_exists = Notification.objects.filter(
            user=self.user,
            message__contains="status changed to Resolved"
        ).exists()
        print(f"Notification exists: {notification_exists}")  # Debugging: Print if notification exists
        self.assertTrue(notification_exists)
        
    def tearDown(self):
        self.client.logout()