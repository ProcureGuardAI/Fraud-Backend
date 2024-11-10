from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contract
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from contract_parser.serializers import ContractSerializer
from django.db import transaction
from utils.utils import extract_text_from_pdf, process_contract_data
import logging

logger = logging.getLogger(__name__)
class ContractParserView(APIView):
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]

    @transaction.atomic
    def post(self, request):
        try:
            # Extract the contract data from the request
            pdf_file = request.FILES.get('pdf_file')
            if pdf_file is not None:
                pdf_file.seek(0)
                text = extract_text_from_pdf(pdf_file)
                contract_data = process_contract_data(text)

                # logging
                logger.debug("Contract data: %s", contract_data)

                # Create a new contract object using the ContractForm
                serializer = ContractSerializer(data=contract_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    # Add debugging information
                    return Response({'error': 'Invalid contract data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'No PDF file provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)