from rest_framework import serializers
from .models import Reports

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'fraud_score', 'is_flagged']
    
    def validate_status(self, value):
        """
        Example custom validation to prevent setting status to 'Resolved'
        directly, unless certain conditions are met.
        """
        if value == 'Resolved' and not self.instance.is_flagged:
            raise serializers.ValidationError("Status can't be set to 'Resolved' without the report being flagged.")
        return value

        fields = ['id', 'title', 'description', 'email', 'prediction', 'created_at']
