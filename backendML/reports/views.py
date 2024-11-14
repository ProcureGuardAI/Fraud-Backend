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

# FILE: reports/views.py

from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def generate_and_send_report(template_name, data, description, pdf_path, recipient_email, prediction_result):
    try:
        template = get_template(template_name)
        report_content = template.render(data)
        
        email = EmailMessage(
            "Contract Report",
            description,
            settings.EMAIL_HOST_USER,
            [recipient_email],
        )
        email.attach("report.html", report_content, "text/html")
        email.body = f"Prediction result: {prediction_result}"

        email.send()
        logger.info("Report sent successfully.")
    except Exception as e:
        logger.error(f"Error sending report: {e}")

# class GenerateReport(APIView):
#     def get(self, request):
#         contracts = Reports.objects.all()
#         serializer = ContractSerializer(contracts, many=True)
#         description = "This is a report of all contracts."
#         pdf_path = request.query_params.get('pdf_path', None)
#         report_builder = ReportBuilder('reports.html', serializer.data, description, pdf_path)
        
#         user_email = request.query_params.get('user_email', 'clency2023@gmail.com')  # Get user email from query params
#         try:
#             report_builder.send_report("Contract Report", user_email)
#             return Response({"message": "Report sent successfully!"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def home(request):
#     return HttpResponse("Welcome to the Home Page")