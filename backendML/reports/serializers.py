from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
<<<<<<< HEAD
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'transaction_id', 'fraud_score', 'is_flagged', 'status']
        read_only_fields = ['created_at', 'updated_at', 'fraud_score', 'is_flagged']
    
    def validate_status(self, value):
        """
        Example custom validation to prevent setting status to 'Resolved'
        directly, unless certain conditions are met.
        """
        if value == 'Resolved' and not self.instance.is_flagged:
            raise serializers.ValidationError("Status can't be set to 'Resolved' without the report being flagged.")
        return value
=======
        fields = ['id', 'title', 'description', 'email', 'prediction', 'created_at']
>>>>>>> e2547b448a2294b3b8149896b509cae05fa862af
