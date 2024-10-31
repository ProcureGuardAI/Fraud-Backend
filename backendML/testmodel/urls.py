# urls.py
from django.urls import path
from .views import TestModelEndpoint

urlpatterns = [
    path('testmodel/', TestModelEndpoint.as_view(), name='testmodel')
]
