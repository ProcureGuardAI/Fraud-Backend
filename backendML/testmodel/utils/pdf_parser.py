import fitz  # PyMuPDF
import requests
import base64
import re
import markdown
import logging
import csv
import io
import joblib  # For loading the local model

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load your local model (e.g., scikit-learn, custom ML model)
model2 = joblib.load('/home/clencyc/Dev/Fraud-Detection-Machine-Learning/Models/best_model_random_forest.pkl')

# Function to extract text from a PDF file
def extract_pdf_contents(pdf_path):
    try:
        document = fitz.open(pdf_path)
        text = ""
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            text += page.get_text()
        logger.info(f"Extracted text: {text[:100]}...")
        return text
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        return None

# Function to base64 encode the extracted file contents
def encode_file_contents(file_contents):
    try:
        encoded_contents = base64.b64encode(file_contents.encode('utf-8')).decode('utf-8')
        logger.info(f"Encoded contents: {encoded_contents[:100]}...")
        return encoded_contents
    except Exception as e:
        logger.error(f"Error encoding file contents: {e}")
        return None

# Function to convert Markdown to plain text
def markdown_to_plain_text(markdown_text):
    html = markdown.markdown(markdown_text)
    plain_text = re.sub('<[^<]+?>', '', html)
    return plain_text

# Function to convert plain text to CSV
def plain_text_to_csv(plain_text):
    output = io.StringIO()
    writer = csv.writer(output)
    lines = plain_text.split('\n')
    for line in lines:
        writer.writerow([line])
    return output.getvalue()

# Function to process the PDF contents
def send_pdf_to_api_and_local(pdf_path):
    file_contents = extract_pdf_contents(pdf_path)
    
    if file_contents:
        # Base64 encode the extracted contents for the first API
        encoded_contents = encode_file_contents(file_contents)
        if encoded_contents is None:
            logger.error("Failed to encode file contents.")
            return
        
        # Data formatted for the first API (expects JSON)
        data = {
            "data": [["file_contents", encoded_contents]]
        }

        # Call the first API
        try:
            response = requests.post(
                "https://christineoyiera.us-east-1.aws.modelbit.com/v1/llama/latest",
                json=data
            )
            if response.status_code == 200:
                logger.info(f"Response from first model: {response.json()}")
                first_model_response = response.json()
            else:
                logger.error(f"Error from first model: {response.status_code}, {response.text}")
                return {"error": f"Error from first model: {response.status_code}, {response.text}"}
        except requests.RequestException as e:
            logger.error(f"Request to first model failed: {e}")
            return {"error": f"Request to first model failed: {e}"}

        # Check if the response data is None
        if first_model_response["data"][0][1] is None:
            logger.error("First model response data is None")
            return {"error": "First model response data is None"}

        # Convert the Markdown content to plain text
        plain_text = markdown_to_plain_text(first_model_response["data"][0][1])

        # Use the local model for the second processing
        try:
            second_model_response = model2.predict([plain_text])[0]  # Adjust as needed for your model
            logger.info(f"Response from local model: {second_model_response}")
        except Exception as e:
            logger.error(f"Error processing with local model: {e}")
            return {"error": f"Error processing with local model: {e}"}

        # Convert the plain text response to CSV
        csv_result = plain_text_to_csv(second_model_response)

        return {
            "first_model_response": first_model_response,
            "second_model_response": csv_result
        }

    else:
        logger.error("No content extracted from the PDF.")
        return {"error": "No content extracted from the PDF."}

# Path to your PDF file
pdf_path = "/home/clencyc/Downloads/Package_1_Lot_2_Kulamawe_Modogashe_Consultancy_Services_Beneficial (1).pdf"

# Call the function to process the PDF
result = send_pdf_to_api_and_local(pdf_path)
logger.info(f"Final result: {result}")
