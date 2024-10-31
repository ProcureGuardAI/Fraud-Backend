# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ml_loader import load_model
import numpy as np
import os
import pickle

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
        # contrectnumber, amount, award date, tender title, eval completion, notification, sign-date, start-date, end-date, 
        contract_number = request.data.get('Contract_number')
        amount = request.data.get('amount')
        # Include any other fields you want to process
        # e.g., award_date, tender_title, eval_completion, etc.
        
        # You can now use these variables to run predictions with your model
        # model_output = your_model.predict([[Contract_number, amount, ...]])
        
        # Just an example response
        response_data = {
            "contract_number": contract_number,
            "amount": amount,
            "model_prediction": 0  # Replace with your model output
            # "award_date": "2021-01-01",
            # "tender_title": "Test Tender",
            # "eval_completion": "2021-01-02",
            # "notification": "2021-01-02",
            # "sign_date": "2021-01-03",
            # "start_date": "2021-01-04",
            # "end_date": "2021-01-05",
            # "financial_year": "2021",
            # "quarter": "Q1",
            # "Tender_ref": "MLPP/4/2016-2017",
            # "Pe_Name": "Ministry of Health",
            # "supplier": "Test Supplier",
            # "created_at": "2021-01-01T00:00:00Z",



            # Include model output or any additional data you want to return
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
     except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)