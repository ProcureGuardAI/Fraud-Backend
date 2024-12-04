# FILE: testmodel/utils/pdf_parser.py

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import requests
import base64
import re
import markdown
import logging
import csv
import joblib  # For loading the local model
from backendML.utils import generate_and_send_report  # Import the generate_report function

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Load your local model (e.g., scikit-learn, custom ML model)
model2 = joblib.load('/home/james/Documents/AI/Fraud-Detection-Machine-Learning/best_model_random_forest.pkl')

# Define the fields to be extracted
fields = [
    "Contract Number", "Amount", "Award Date", "Tender Title", "Eval Completion Date", 
    "Notification Of Award Date", "Sign Date", "Start Date", "End Date", 
    "Agpo Certificate Number", "Awarded Agpo Group Id", "Created By", "Terminated", 
    "Financial Year", "Quarter", "Tender Ref.", "PE Name", "Supplier Name"
]

# Function to extract text from a PDF file
def extract_pdf_contents(pdf_path):
    try:
        # Open the PDF
        document = fitz.open(pdf_path)
        text = ""
        
        # Extract text from each page
        for page_num in range(len(document)):
            try:
                page = document[page_num]
                page_text = page.get_text()
                logger.debug(f"Extracted text from page {page_num}: {page_text}")
                text += page_text
                
                # If no text is found, try OCR
                if not page_text.strip():
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    ocr_text = pytesseract.image_to_string(img)
                    logger.debug(f"OCR text from page {page_num}: {ocr_text}")
                    text += ocr_text
            except Exception as e:
                logger.error(f"Error processing page {page_num}: {e}")
        
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

# Update the plain_text_to_features function to keep only the required features
REQUIRED_FEATURE_COUNT = 19  # Change this as per your model’s needs

def plain_text_to_features(plain_text):
    try:
        # Extract numeric values from the plain text
        all_features = [float(x) for x in re.findall(r'\b\d+\.\d+\b|\b\d+\b', plain_text)]
        
        # Ensure only the first 19 features are passed, or handle accordingly
        features = all_features[:REQUIRED_FEATURE_COUNT]
        if len(features) < REQUIRED_FEATURE_COUNT:
            logger.error("Insufficient number of features extracted.")
            return None
        
        logger.info(f"Extracted features: {features}")
        logger.info(f"Number of features: {len(features)}")
        
        return features
    except Exception as e:
        logger.error(f"Error converting plain text to features: {e}")
        return None

# Function to convert plain text to CSV
def plain_text_to_csv(plain_text):
    if not isinstance(plain_text, str):
        logger.error("Expected plain text, but received non-string input.")
        return None  # or handle this case as needed
    try:
        lines = plain_text.split('\n')
        output = io.StringIO()
        writer = csv.writer(output)
        for line in lines:
            writer.writerow([line])
        return output.getvalue()
    except Exception as e:
        logger.error(f"Error converting plain text to CSV: {e}")
        return None

# Function to process the PDF contents
def send_pdf_to_api_and_local(pdf_path):
    file_contents = extract_pdf_contents(pdf_path)
    
    if file_contents:
        # Base64 encode the extracted contents for the first API
        encoded_contents = encode_file_contents(file_contents)
        if encoded_contents is None:
            logger.error("Failed to encode file contents.")
            return {"error": "Failed to encode file contents."}
        
        # Data formatted for the first API (expects JSON)
        data = {
            "data": [["file_contents", encoded_contents]]
        }

        # Call the first API
        try:
            response = requests.post(
                "https://christineoyiera.us-east-1.aws.modelbit.com/v1/llama/19",
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

        # Convert the plain text to structured data (list of floats)
        features = plain_text_to_features(plain_text)
        if features is None:
            logger.error("Failed to convert plain text to features")
            return {"error": "Failed to convert plain text to features"}

        # Use the local model for the second processing
        try:
            logger.info(f"Features for local model: {features}")
            second_model_response = model2.predict([features])[0]  # Adjust as needed for your model
            logger.info(f"Response from local model: {second_model_response}")
            second_model_response = int(second_model_response)  # Convert numpy.int64 to int
        except Exception as e:
            logger.error(f"Error processing with local model: {e}")
            return {"error": f"Error processing with local model: {e}"}
        logger.info(f"Extracted features (first 5): {features[:5]}...")

        return {
            "first_model_response": first_model_response,
            "second_model_response": second_model_response,
            "features_used_for_prediction": features  # Add this to see the features used for prediction
        }
    else:
        logger.error("No content extracted from the PDF.")
        return {"error": "No content extracted from the PDF."}
