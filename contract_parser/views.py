from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from.models import Contract
from.serializers import ContractSerializer
from django.db import transaction
from contract_parser.utils import extract_text_from_pdf, process_contract_data

class ContractParserView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            # Extract the contract data from the request
            pdf_file = request.FILES['pdf_file']

            # Extract the text from the PDF file
            text = extract_text_from_pdf(pdf_file)

            # Process the extracted text
            contract_data = process_contract_data(text)

            # Create a new contract object
            contract = Contract.objects.create(**contract_data)

            # Serialize the contract data
            serializer = ContractSerializer(contract)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)