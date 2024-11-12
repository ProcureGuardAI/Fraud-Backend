from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import requests
import logging
import re
import json

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# URLs for the Llama and external prediction models
LLAMA_MODEL_URL = "https://christineoyiera.us-east-1.aws.modelbit.com/v1/llama/latest"
EXTERNAL_MODEL_URL = "https://christineoyiera.us-east-1.aws.modelbit.com/v1/predict/latest"

def extract_text_from_markdown(markdown_content):
    """Utility to convert Markdown text to plain text by stripping Markdown syntax."""
    plain_text = re.sub(r'[_*`]', '', markdown_content)
    return plain_text

class TestModelEndpoint(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'file' not in request.FILES:
            logger.error("PDF file is required but not found in the request.")
            return Response({"error": "PDF file is required."}, status=status.HTTP_400_BAD_REQUEST)

        pdf_file = request.FILES['file']
        try:
            # Log the request data
            logger.info(f"Sending PDF file to Llama model: {pdf_file.name}")

            llama_response = requests.post(
                LLAMA_MODEL_URL,
                files={"file": pdf_file},
                timeout=10
            )
            logger.info(f"Llama model full response: {llama_response.text}")

            # Attempt to parse the response as JSON
            try:
                response_data = json.loads(llama_response.text)
                logger.info(f"Llama model JSON response: {response_data}")

                # Handle known error field directly if present
                if "error" in response_data:
                    error_message = response_data["error"]
                    
                    # Check if the error message itself is JSON-like (e.g., nested JSON as a string)
                    try:
                        nested_error = json.loads(error_message)
                        if "error" in nested_error:
                            logger.error(f"Llama model returned a nested error: {nested_error['error']}")
                            return Response({"error": nested_error["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    except json.JSONDecodeError:
                        # If nested error is not JSON, return the raw error message
                        logger.error(f"Llama model error: {error_message}")
                        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Proceed to extract main content if no error was found
                processed_text = response_data.get("processed_text") or response_data.get("text") or response_data.get("data")
                if not processed_text:
                    logger.error("Neither 'processed_text' nor alternative fields found in Llama response.")
                    return Response(
                        {"error": "Processed text not found in Llama response.", "details": response_data},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            except json.JSONDecodeError as e:
                # Handle JSON decoding error and fall back to plain text handling
                logger.error(f"Primary JSON parsing error: {e}")
                processed_text = extract_text_from_markdown(llama_response.text)
                logger.info("Processed response as plain text due to JSON decoding error.")

            # Send processed text to the external model if available
            if processed_text:
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
            else:
                return Response({"error": "Failed to process Llama response"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Llama model: {e}")
            return Response({"error": "Failed to connect to Llama model", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
