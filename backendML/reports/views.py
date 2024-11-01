from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Report
from .serializers import ReportSerializer
from django.core.mail import send_mail
from testmodel.ml_loader import load_model
import numpy as np
import pandas as pd

model = load_model()

class GenerateReportView(APIView):
    def post(self, request):
        try:
            # Read the request data
            data = request.data
            email = data.get('email')
            title = data.get('title')
            description = data.get('description')
            input_data = data.get('input_data')

            # Convert input data to DataFrame
            input_df = pd.DataFrame([input_data])

            # Run the prediction
            prediction = model.predict(input_df)[0]

            # Save the report
            report = Report(
                title=title,
                description=description,
                email=email,
                prediction=prediction
            )
            report.save()

            # Send the report via email
            send_mail(
                'Your Report',
                f'Title: {title}\nDescription: {description}\nPrediction result: {prediction}',
                'from@example.com',
                [email],
                fail_silently=False,
            )

            # Serialize the report
            serializer = ReportSerializer(report)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
