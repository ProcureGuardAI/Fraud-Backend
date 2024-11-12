# urls.py
from django.urls import path
from .views import handle_pdf_upload

urlpatterns = [
    # path('testmodel/', TestModelEndpoint.as_view(), name='testmodel'),
    path('api/upload_pdf/', handle_pdf_upload, name='upload_pdf'),
]

# check on the market value