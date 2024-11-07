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