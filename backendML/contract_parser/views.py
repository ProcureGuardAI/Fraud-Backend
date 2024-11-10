from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from.models import Contract
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from contract_parser.serializers import ContractSerializer
from django.db import transaction
import PyPDF2
from django.shortcuts import render, redirect
from utils.utils import extract_text_from_pdf, process_contract_data
from .forms import ContractForm


def create_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contract_list')
    else:
        form = ContractForm()
    return render(request, 'contract_form.html', {'form': form})
		

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

                # Create a new contract object using the ContractForm
                form = ContractForm(contract_data)
                if form.is_valid():
                    contract = form.save()
                    serializer = ContractSerializer(contract)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                        # Add debugging information
                    return Response({'error': 'Invalid contract data', 'details': form.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'No PDF file provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)