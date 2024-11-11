from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from json import JSONDecodeError
import requests
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# URLs for the Llama and external prediction models
LLAMA_MODEL_URL = "https://christineoyiera.us-east-1.aws.modelbit.com/v1/llama/latest"
EXTERNAL_MODEL_URL = "https://christineoyiera.us-east-1.aws.modelbit.com/v1/predict/latest"

class TestModelEndpoint(APIView):
    def post(self, request):
        try:
            # Check if PDF file is in the request
            if 'file' not in request.FILES:
                logger.error("PDF file is required but not found in the request.")
                return Response({"error": "PDF file is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Send PDF file to Llama model
            pdf_file = request.FILES['file']
            llama_response = requests.post(
                LLAMA_MODEL_URL,
                files={"file": pdf_file},
                timeout=10
            )

            if llama_response.status_code != 200:
                logger.error(f"Failed to process PDF with Llama model: {llama_response.text}")
                return Response({"error": "Failed to process PDF with Llama model", "details": llama_response.text}, status=llama_response.status_code)

            # Get processed text from Llama response
            processed_text = llama_response.json().get("processed_text")
            if not processed_text:
                logger.error("Processed text not found in Llama response.")
                return Response({"error": "Processed text not found in Llama response."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Send processed text to the external prediction model
            prediction_response = requests.post(
                EXTERNAL_MODEL_URL,
                json={"data": processed_text},
                timeout=5
            )

            if prediction_response.status_code == 200:
                external_prediction = prediction_response.json().get("prediction")
                logger.info("Prediction successful (external model).")
                return Response({
                    "message": "Prediction successful (external model)",
                    "prediction": external_prediction
                }, status=status.HTTP_200_OK)
            else:
                logger.error(f"External model request failed with status {prediction_response.status_code}: {prediction_response.text}")
                return Response({
                    "error": f"External model request failed with status {prediction_response.status_code}",
                    "details": prediction_response.text
                }, status=prediction_response.status_code)

        except JSONDecodeError:
            logger.error("Invalid JSON format in the response.")
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {str(e)}")
            return Response({"error": "Request failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)