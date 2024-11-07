
from django.test import TestCase

# Create your tests here.

# # report_builder/tests/test_views.py
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import Contract
# from .serializers import ContractSerializer

# class GenerateReportTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.contract1 = Contract.objects.create(name="Contract 1", details="Details of contract 1")
#         self.contract2 = Contract.objects.create(name="Contract 2", details="Details of contract 2")
#         self.valid_payload = {
#             'user_email': 'test@example.com'
#         }

#     def test_generate_report_success(self):
#         response = self.client.get(reverse('generate_report'), self.valid_payload)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("Report sent successfully!", response.data['message'])

#     def test_generate_report_missing_email(self):
#         response = self.client.get(reverse('generate_report'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("Report sent successfully!", response.data['message'])

#     def test_generate_report_invalid_email(self):
#         invalid_payload = {
#             'user_email': 'invalid-email'
#         }
#         response = self.client.get(reverse('generate_report'), invalid_payload)
#         self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
#         self.assertIn("Failed to send report", response.data['error'])