# urls.py
from django.urls import path
from .views import TestModelEndpoint

urlpatterns = [
    path('test-model/', TestModelEndpoint.as_view(), name='test-model')
]
