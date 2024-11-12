from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import requests
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import logging

# # Configure logging
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

# # URLs for the Llama and external prediction models

# LLAMA_MODEL_URL = "https://christineoyiera.us-east-1.aws.modelbit.com/v1/llama/latest"
# EXTERNAL_MODEL_URL = "https://christineoyiera.us-east-1.aws.modelbit.com/v1/predict/latest"

# class TestModelEndpoint(APIView):
#     parser_classes = [MultiPartParser, FormParser]  # Correct: use for request parsing
#     renderer_classes = [JSONRenderer] 
#     def post(self, request):
#         try:
#             # Check if PDF file is in the request
#             if 'file' not in request.FILES:
#                 logger.error("PDF file is required but not found in the request.")
#                 return Response({"error": "PDF file is required."}, status=status.HTTP_400_BAD_REQUEST)
            
#             # Send PDF file to Llama model
#             pdf_file = request.FILES['file']
#             llama_response = requests.post(
#                 LLAMA_MODEL_URL,
#                 files={"file": pdf_file},
#                 timeout=10
#             )

#             # Log the full response from the Llama model
#             logger.info(f"Llama model response status: {llama_response.status_code}")
#             logger.info(f"Llama model response headers: {llama_response.headers}")
#             logger.info(f"Llama model response text: {llama_response.text}")

#             if llama_response.status_code != 200:
#                 logger.error(f"Failed to process PDF with Llama model: {llama_response.text}")
#                 return Response({"error": "Failed to process PDF with Llama model", "details": llama_response.text}, status=llama_response.status_code)

#             # Extract the Markdown content from the response
#             processed_text = llama_response.text

#             if not processed_text:
#                 logger.error("Processed text not found in Llama response.")
#                 return Response({"error": "Processed text not found in Llama response."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#             try:
#                 processed_text = llama_response.json()  # Attempt to parse as JSON
#             except ValueError:
#                 logger.error("Response from Llama model is not valid JSON.")
#                 processed_text = llama_response.text  # Fallback to raw text
            
#             if not processed_text:
#                 logger.error("Processed text not found in Llama response.")
#                 return Response({"error": "Processed text not found in Llama response."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Process the Markdown content if necessary
#             # For example, you can convert it to plain text or HTML
#             # Here, we assume the processed_text is already in a usable format

#             # Send processed text to the external prediction model
#             prediction_response = requests.post(
#                 EXTERNAL_MODEL_URL,
#                 json={"data": processed_text},
#                 timeout=5
#             )

#             if prediction_response.status_code == 200:
#                 external_prediction = prediction_response.json().get("prediction")
#                 logger.info("Prediction successful (external model).")
#                 return Response({
#                     "message": "Prediction successful (external model)",
#                     "prediction": external_prediction
#                 }, status=status.HTTP_200_OK)
#             else:
#                 logger.error(f"External model request failed with status {prediction_response.status_code}: {prediction_response.text}")
#                 return Response({
#                     "error": f"External model request failed with status {prediction_response.status_code}",
#                     "details": prediction_response.text
#                 }, status=prediction_response.status_code)

#         except requests.exceptions.RequestException as e:
#             logger.error(f"Request exception: {str(e)}")
#             return Response({"error": "Request failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except Exception as e:
#             logger.error(f"An unexpected error occurred: {str(e)}")
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
