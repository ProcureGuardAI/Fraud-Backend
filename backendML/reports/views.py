<<<<<<< HEAD
from rest_framework import viewsets, permissions # type: ignore
from .models import Report
from .serializers import ReportSerializer
from .tasks import run_fraud_detection

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        report = serializer.save(created_by=self.request.user)
        run_fraud_detection(report)  # Call ML function to detect fraud
        return report

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_status = instance.status
        response = super().update(request, *args, **kwargs)

        # Notification logic removed since it's handled by signals
        return response
=======
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
>>>>>>> e2547b448a2294b3b8149896b509cae05fa862af
