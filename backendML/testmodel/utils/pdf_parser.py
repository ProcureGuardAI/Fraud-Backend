import fitz  # PyMuPDF
import requests
import base64

# Function to extract text from a PDF file
def extract_pdf_contents(pdf_path):
    try:
        # Open the PDF
        document = fitz.open(pdf_path)
        text = ""
        
        # Extract text from each page
        for page_num in range(document.page_count):
            page = document.load_page(page_num)
            text += page.get_text()
        
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# Function to base64 encode the extracted file contents
def encode_file_contents(file_contents):
    try:
        return base64.b64encode(file_contents.encode('utf-8')).decode('utf-8')
    except Exception as e:
        print(f"Error encoding file contents: {e}")
        return None

# Function to call the API with the extracted text, formatted as required
def send_pdf_to_api(pdf_path):
    file_contents = extract_pdf_contents(pdf_path)
    
    if file_contents:
        # Base64 encode the extracted contents
        encoded_contents = encode_file_contents(file_contents)
        
        if encoded_contents is None:
            print("Failed to encode file contents.")
            return
        
        # Format the data as a list of lists, as expected by the API
        data = [
            ["file_contents", encoded_contents]  # Pass base64-encoded contents
        ]
        
        # Define the API URLs
        api_url_1 = "https://christineoyiera.us-east-1.aws.modelbit.com/v1/llama/latest"
        api_url_2 = "https://christineoyiera.us-east-1.aws.modelbit.com/v1/predict/1"
        
        # Call the first API
        try:
            response = requests.post(api_url_1, json={"data": data})
            if response.status_code == 200:
                print("Response from first model:", response.json())
            elif response.status_code == 400:
                print("Error: Bad request to the first model")
            elif response.status_code == 500:
                print("Error: Internal server error in the first model")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except requests.RequestException as e:
            print(f"Request to first model failed: {e}")
        
        # Call the second API
        try:
            response = requests.post(api_url_2, json={"data": data})
            if response.status_code == 200:
                print("Response from second model:", response.json())
            elif response.status_code == 400:
                print("Error: Bad request to the second model")
            elif response.status_code == 500:
                print("Error: Internal server error in the second model")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        except requests.RequestException as e:
            print(f"Request to second model failed: {e}")
    else:
        print("No content extracted from the PDF.")

# Path to your PDF file
pdf_path = "/home/clencyc/Dev/Llama_Parse/Untitled_document.pdf"

# Call the function to send the PDF contents to the API
send_pdf_to_api(pdf_path)
