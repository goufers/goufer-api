# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Wallet, Transaction, Bank
from .serializers import WalletSerializer, TransactionSerializer, BankSerializer, FundWalletSerializer, TransferFundsSerializer
import requests
from decimal import Decimal
from django.conf import settings
from rest_framework.views import APIView
from user.models import CustomUser

paystack_secret_key = 'sk_test_58d7c6da2b1b3fb1c246d71e090cc18d76221624'


class FundWalletView(APIView):
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
            print(response_data)
            if response_data['status']:
                authorization_url = response_data['data']['authorization_url']
                reference = response_data['data']['reference']
                result = self.verify_payment(request, reference)
                print(result)
                return Response({'authorization_url': authorization_url})
            else:
                return Response({'error': 'Unable to initialize transaction.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'ERROR':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def verify_payment(self, request, reference):
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

# class DashboardView(APIView):
#     """User dashboard used for test"""
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         wallet = Wallet.objects.filter(user=user).first()
#         wallet_serializer = WalletSerializer(wallet)
#         return Response({'user': user.username, 'wallet': wallet_serializer.data})
