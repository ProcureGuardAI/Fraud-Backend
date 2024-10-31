# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ml_loader import load_model
import numpy as np
import os
import pickle
import pandas as pd

model = load_model()

class TestModelEndpoint(APIView):
    def get(self, request):
        try:
            # Load the model
           

            # Test prediction (update `test_input` based on your model’s expected input format)
            test_input = np.array([[0]])  # Modify if your model requires a different shape
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
            # Extract and organize test data from the request
            test_data = request.data.get("data")  # Expecting a JSON format containing necessary fields
            
            # Convert input to DataFrame
            input_df = pd.DataFrame([test_data])  # Wrap in list to create single row DataFrame
            
            # Ensure input columns match the model's expected format
            input_df = input_df.reindex(columns=model.feature_names_in_, fill_value=0)  # Adjust for column order
            
            # Run the prediction
            prediction = model.predict(input_df)
            
            return Response({
                "message": "Prediction successful",
                "prediction": int(prediction[0])  # Assuming binary output 0 for 'not fraud', 1 for 'fraud'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)