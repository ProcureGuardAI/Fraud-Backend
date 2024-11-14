from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from .models import Reports
from .serializers import ContractSerializer
from backendML.settings import EMAIL_HOST_USER
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template
from testmodel.utils.pdf_parser import send_pdf_to_api_and_local
import logging


class ReportBuilder:
    def __init__(self, template_name, data, description, pdf_path=None):
        self.template_name = template_name
        self.data = data
        self.description = description
        self.pdf_path = pdf_path

    def generate_report(self):
        # Instead of rendering a template, return the data directly
        template = get_template(self.template_name)
        return template.render(self.data)
    
    def send_report(self, subject, recipient_email):
        # Implement the email sending logic here
        try:
            email = EmailMessage(
                subject,
                self.description,
                settings.EMAIL_HOST_USER,
                [recipient_email],
            )
            email.attach(self.generate_report())

            if self.pdf_path:
                prediction_result = send_pdf_to_api_and_local(self.pdf_path)
                email.body = f"Prediction result: {prediction_result}"

            email.send()
        except Exception as e:
            print(f"Error sending email: {e}")


class GenerateReport(APIView):
    def get(self, request):
        contracts = Reports.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        description = "This is a report of all contracts."
        pdf_path = request.query_params.get('pdf_path', None)
        report_builder = ReportBuilder('reports.html', serializer.data, description, pdf_path)
        
        user_email = request.query_params.get('user_email', 'clency2023@gmail.com')  # Get user email from query params
        try:
            report_builder.send_report("Contract Report", user_email)
            return Response({"message": "Report sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def home(request):
    return HttpResponse("Welcome to the Home Page")