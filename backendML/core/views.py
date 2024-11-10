from rest_framework import viewsets
from .models import Transaction  # Import the concrete model
from .serializers import TransactionSerializer  # Import the corresponding serializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()  # Queryset for the concrete model
    serializer_class = TransactionSerializer  # Serializer for the concrete model

def admin(request):
    return redirect('/admin')

def users(request):
    return redirect('/api/users')

def notifications(request):
    return redirect('/api/notifications')

def reports(request):
    return redirect('/api/reports')
