from django.urls import path, include
from .views import ContractParserView

urlpatterns = [
    path('contracts/', ContractParserView.as_view(), name='contract-parser'),
]
