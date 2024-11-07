from .serializers import RegisterSerializer
from .models import User
from django.http import JsonResponse # type: ignore
from rest_framework.parsers import JSONParser # type: ignore
from rest_framework import views, status # type: ignore
from rest_framework.response import Response # type: ignore
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.views import APIView # type: ignore
from django.contrib.auth import login # type: ignore
from json import JSONDecodeError
import json


class RegisterAPIView(APIView):
    """
    A simple APIView for registering a new user.
    """
    serializer_class = RegisterSerializer # used to get access to the serializer class

    # def get_serializer_context(self):
    #     return {
    #         'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }

    # def get_serializer(self, *args, **kwargs):
    #     kwargs['context'] = self.get_serializer_context()
    #     return self.serializer_class(*args, **kwargs)
    
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
            return JsonResponse({"result":"error", "message":"Json decoding error"}, status=400)
        

class LoginAPIView(APIView):
    """
    A simple APIView for logging in a user.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            print(data)
            email = data.get('email')
            password = data.get('password')

            user = User.objects.filter(email=email).first()
            if user is None:
                return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = LoginSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                print("Serializer errors:", serializer.errors)  # Log serializer errors for debugging
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return JsonResponse({"result": "error", "message": "JSON decoding error"}, status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")  # Log any other exceptions
            return JsonResponse({"result": "error", "message": str(e)}, status=400)
