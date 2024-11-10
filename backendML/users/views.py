from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import User
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from json import JSONDecodeError
import json

class RegisterAPIView(APIView):
    """
    A simple APIView for registering a new user.
    """
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "JSON decoding error"}, status=400)

class LoginAPIView(APIView):
    """
    A simple APIView for logging in a user.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            email = data.get('email')
            password = data.get('password')

            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = LoginSerializer(data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                login(request, user)

                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "JSON decoding error"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"result": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user