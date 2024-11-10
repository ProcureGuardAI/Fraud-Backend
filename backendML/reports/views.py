from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import Reports
from .serializers import ContractSerializer
from backendML.settings import EMAIL_HOST_USER
from django.http import HttpResponse
from django.conf import settings


class ReportBuilder:
    def __init__(self, template_name, data, description):
        self.template_name = template_name
        self.data = data
        self.description = description

    def generate_report(self):
        # Instead of rendering a template, return the data directly
        return self.data
    
    def send_report(self, subject, recipient_email):
        # Implement the email sending logic here
        send_mail(
            subject,
            self.description,
            settings.EMAIL_HOST_USER,
            [recipient_email],
            fail_silently=False,
        )


class GenerateReport(APIView):
    def get(self, request):
        contracts = Reports.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        description = "This is a report of all contracts."
        report_builder = ReportBuilder('reports.html', serializer.data, description)
        
        user_email = request.query_params.get('user_email', 'clency2023@gmail.com')  # Get user email from query params
        try:
            report_builder.send_report("Contract Report", user_email)
            return Response({"message": "Report sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def home(request):
    return HttpResponse("Welcome to the Home Page")