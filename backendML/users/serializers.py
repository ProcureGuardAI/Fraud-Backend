from rest_framework import serializers
from .models import User  # Ensure you import your custom User model if you have one

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'full_name', 'phone_number', 'role', 'department', 'office_location', 'security_question', 'two_fa']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role'],
            department=validated_data['department'],
            office_location=validated_data['office_location'],
            security_question=validated_data['security_question'],
            two_fa=validated_data['two_fa']
        )
        return user