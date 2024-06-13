# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser,
    IsAuthenticatedOrReadOnly
    )
from django.shortcuts import get_object_or_404
from .models import (
    Wallet, Transaction, Bank, 
    Hour, Day, Schedule
    )
from .serializers import (
    WalletSerializer, TransactionSerializer, BankSerializer, 
    FundWalletSerializer, TransferFundsSerializer,
    HourSerializer, DaySerializer, ScheduleSerializer
    )
import requests
from decimal import Decimal
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import viewsets
from user.models import CustomUser
from django.db.models import Count


paystack_secret_key = 'sk_test_58d7c6da2b1b3fb1c246d71e090cc18d76221624'


class FundWalletView(APIView):
    """Fund user wallet."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = FundWalletSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(CustomUser, pk=request.user.pk)
            amount = serializer.validated_data['amount']
            email = request.user.email
            url = 'https://api.paystack.co/transaction/initialize'
            headers = {
                'Authorization': f'Bearer {paystack_secret_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'email': email,
                'amount': int(amount * 100)  # Paystack expects the amount in kobo
            }
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            if response_data['status']:
                authorization_url = response_data['data']['authorization_url']
                reference = response_data['data']['reference']
                result = self.verify_payment(request, reference) # Verify payment before updating wallet
                return Response({'authorization_url': authorization_url, 'amount': data['amount']}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Unable to initialize transaction.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'ERROR':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def verify_payment(self, request, reference):
        """Verify payment before updating wallet."""
        url = f'https://api.paystack.co/transaction/verify/{reference}'
        headers = {
            'Authorization': f'Bearer {paystack_secret_key}',
        }
        response = requests.get(url, headers=headers)
        response_data = response.json()
        print(response_data)
        if response_data['status']:
            amount = response_data['data']['amount'] / 100  # Convert from kobo to naira
            wallet = Wallet.objects.filter(user=request.user).first()
            wallet.balance += Decimal(amount)
            wallet.save()
            Transaction.objects.create(wallet=wallet, amount=amount, transaction_type='deposit')
            return Response({'success': True,
                             'user': request.user.username,
                             'amount': amount}, status=status.HTTP_201_CREATED)


class CreateTransferRecipientView(APIView):
    """Create a transfer recipient."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            bank_code = request.data.get('bank_code')
            account_number = request.data.get('account_number')
            name = request.data.get('name')

            url = 'https://api.paystack.co/transferrecipient'
            headers = {
                'Authorization': f'Bearer {paystack_secret_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'type': 'nuban',
                'name': name,
                'account_number': account_number,
                'bank_code': bank_code,
                'currency': 'NGN'
            }
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            if response_data['status']:
                recipient_code = response_data['data']['recipient_code']
                Bank.objects.create(
                    user=request.user,
                    recipient_code=recipient_code,
                    bank_name=name,
                    account_number=account_number
                )
                return Response({'message': 'Transfer recipient created successfully.'})
            else:
                return Response({'error': 'Unable to create transfer recipient.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferFundsView(APIView):
    """Transfer funds from user to goufer or errandboy."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferFundsSerializer(data=request.data)
        if serializer.is_valid():
            recipient_username = serializer.validated_data['recipient']
            amount = serializer.validated_data['amount']
            sender_wallet = Wallet.objects.filter(user=request.user).first()
            recipient = get_object_or_404(settings.AUTH_USER_MODEL, username=recipient_username) # Evaluates to either custom user, goufer or errandboy
            recipient_wallet = Wallet.objects.filter(user=recipient).first()

            if sender_wallet.balance >= amount:
                sender_wallet.balance -= amount
                recipient_wallet.balance += amount
                sender_wallet.save()
                recipient_wallet.save()
                Transaction.objects.create(wallet=sender_wallet, amount=amount, transaction_type='transfer')
                Transaction.objects.create(wallet=recipient_wallet, amount=amount, transaction_type='transfer')
                return Response({'message': 'Transfer successful.'})
            else:
                return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HourViewSet(viewsets.ModelViewSet):
    """Hours viewset"""
    queryset = Hour.objects.all()
    serializer_class = HourSerializer

    def get_permissions(self):
        """Only Admins should be able to create or modify work hour"""
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return (IsAuthenticatedOrReadOnly(),)
        return [IsAdminUser]


class DayViewSet(viewsets.ModelViewSet):
    """Days viewset"""
    queryset = Day.objects.all()
    serializer_class = DaySerializer

    def get_permissions(self):
        """Only Admins should be able to create or modify week days"""
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return (IsAuthenticatedOrReadOnly(),)
        return [IsAdminUser]


class ScheduleViewSet(viewsets.ModelViewSet):
    """Schedule viewset"""
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    