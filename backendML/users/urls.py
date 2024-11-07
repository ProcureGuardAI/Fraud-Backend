# users/urls.py
from django.urls import path
from .views import RegisterAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register_user'),
    path('login/', LoginAPIView.as_view(), name='login'),
    # path('api-token-auth/',)

]