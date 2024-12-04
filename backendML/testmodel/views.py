# FILE: testmodel/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .utils.pdf_parser import send_pdf_to_api_and_local  # Import your PDF parsing function
from backendML.utils import generate_and_send_report  # Import the generate_report function
from reports.models import Reports
from reports.serializers import ContractSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_pdf_upload(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        uploaded_file = request.FILES['pdf_file']

        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Process the PDF
        result = send_pdf_to_api_and_local(temp_file_path)

        # Check for errors in the result
        if "error" in result:
            return JsonResponse({"status": "error", "message": result["error"]}, status=400)

        # Generate and send the report
        contracts = Reports.objects.all()
        serializer = ContractSerializer(contracts, many=True)
        description = "This is a report of all contracts."
        
        user_email = request.user.email  # Use authenticated user's email
        try:
            generate_and_send_report('reports.html', serializer.data, description, temp_file_path, user_email, result)
            return JsonResponse({"status": "success", "second_model_response": result["second_model_response"]})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "No file uploaded"}, status=400)