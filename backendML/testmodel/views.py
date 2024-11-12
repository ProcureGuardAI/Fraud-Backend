from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.pdf_parser import send_pdf_to_api  # Import your PDF parsing function

@csrf_exempt
def handle_pdf_upload(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        uploaded_file = request.FILES['pdf_file']

        # Save the uploaded file temporarily
        file_path = f'/tmp/{uploaded_file.name}'
        with open(file_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Process the PDF
        result = send_pdf_to_api(file_path)

        # Return the API response to React
        return JsonResponse({"status": "success", "result": result})
    return JsonResponse({"status": "error", "message": "No file uploaded"}, status=400)
