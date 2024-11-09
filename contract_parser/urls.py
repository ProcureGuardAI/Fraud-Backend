from django.urls import path
from.views import ContractParserView

urlpatterns = [
    path('contract-parser/', ContractParserView.as_view()),
]