from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.pdf_parser import send_pdf_to_api  # Import your PDF parsing function
import tempfile

@csrf_exempt
def handle_pdf_upload(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        uploaded_file = request.FILES['pdf_file']

        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Process the PDF
        result = send_pdf_to_api(temp_file_path)

        # Return the API response to React
        return JsonResponse({"status": "success", "result": result})
    return JsonResponse({"status": "error", "message": "No file uploaded"}, status=400)