from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ml_loader import load_model
import numpy as np
from rest_framework.parsers import JSONParser
from json import JSONDecodeError
import pandas as pd
from sklearn.preprocessing import LabelEncoder

model = load_model()

# Define label encoders for categorical features
label_encoders = {
    'Contract Number': LabelEncoder(),
    'Tender Title': LabelEncoder(),
    'Financial Year': LabelEncoder(),
    'Quarter': LabelEncoder(),
    'Tender Ref.': LabelEncoder(),
    'PE Name': LabelEncoder(),
    'Supplier Name': LabelEncoder()
}

# Fit label encoders with some example data (this should be done with your actual data)
example_data = {
    'Contract Number': ['C001', 'C002'],
    'Tender Title': ['Office Supplies', 'IT Equipment'],
    'Financial Year': ['2023/2024', '2022/2023'],
    'Quarter': ['Q1', 'Q2'],
    'Tender Ref.': ['T2023-001', 'T2022-002'],
    'PE Name': ['Ministry of Education', 'Ministry of Health'],
    'Supplier Name': ['ABC Supplies Ltd', 'XYZ Tech Ltd']
}

for feature, encoder in label_encoders.items():
    encoder.fit(example_data[feature])

class TestModelEndpoint(APIView):
    def get(self, request):
        try:
            # Test prediction (update `test_input` based on your model’s expected input format)
            test_input = np.zeros((1, 19))  # Modify to match the number of features expected by your model
            prediction = model.predict(test_input)

            return Response({
                "message": "Model loaded and test prediction successful",
                "prediction": prediction[0]  # Modify if model returns multi-dimensional output
            }, status=status.HTTP_200_OK)

        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            # Read the request data once
            data = JSONParser().parse(request)
            # Extract and organize test data from the request
            test_data = data.get("data")  # Expecting a JSON format containing necessary fields
            
            # Convert input to DataFrame
            input_df = pd.DataFrame([test_data])  # Wrap in list to create single row DataFrame
            
            # Encode categorical features
            for feature, encoder in label_encoders.items():
                if feature in input_df.columns:
                    input_df[feature] = encoder.transform(input_df[feature])
            
            # Convert date features to numerical values (e.g., timestamps)
            date_features = [
                'Award Date', 'Eval Completion Date', 'Notification Of Award Date',
                'Sign Date', 'Start Date', 'End Date', 'Created At', 'Formatted Start Date', 'Formatted End Date'
            ]
            for feature in date_features:
                if feature in input_df.columns:
                    input_df[feature] = pd.to_datetime(input_df[feature]).map(pd.Timestamp.toordinal)
            
            # Ensure input has the correct number of features
            expected_features = 19  # Update this to match the number of features expected by your model
            if input_df.shape[1] != expected_features:
                return Response({"error": f"Input data must have {expected_features} features"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Run the prediction
            prediction = model.predict(input_df)
            
            return Response({
                "message": "Prediction successful",
                "prediction": int(prediction[0])  # Assuming binary output 0 for 'not fraud', 1 for 'fraud'
            }, status=status.HTTP_200_OK)
        
        except JSONDecodeError as e:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)