# views.py
from pprint import pprint
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, IsAdminUser,
    IsAuthenticatedOrReadOnly
    )
from django.shortcuts import get_object_or_404
from .models import (
    Wallet, Transaction, Bank, Schedule, ProGofer, Booking, MessagePoster
    )

from .serializers import (
    BankSerializer, 
    FundWalletSerializer, TransferFundsSerializer,
    ScheduleSerializer, BookingSerializer,
    TransactionSerializer
    )
import requests
from decimal import Decimal
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import viewsets
from user.models import CustomUser, Gofer
from django.db.models import Count


paystack_secret_key = 'sk_test_1a2483045f4961552f4f516ae5cfd2e0ef9c2fbf'


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
                return Response({'authorization_url': authorization_url, 'amount': data['amount']/100}, status=status.HTTP_201_CREATED)
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
        pprint(response_data)
        if response_data['status']:
            amount = response_data['data']['amount'] / 100  # Convert from kobo to naira
            wallet = Wallet.objects.filter(custom_user=request.user).first()
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
                    custom_user=request.user,
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
            recipient_email = serializer.validated_data['email']
            amount = serializer.validated_data['amount']
            sender_wallet = Wallet.objects.filter(user=request.user).first()
            recipient = get_object_or_404(CustomUser, email=recipient_email) # transfer can be to a gofer, errand boy or progofer
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


class TransactionListView(APIView):
    """List all transactions for authenticated user."""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        transactions = Transaction.objects.filter(wallet__custom_user=request.user).order_by('-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ScheduleCreateView(APIView):
    """Create a new schedule"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        if not isinstance(user, ProGofer):
            return Response({'error': 'Sorry, you do not have permission to create schedules.'}, status=status.HTTP_403_FORBIDDEN)
        
        # user = get_object_or_404(ProGofer, pk=request.user.pk)
        data = request.data.copy()
        data['gofer'] = request.user.id
        serializer = ScheduleSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List schedules for the authenticated user"""
        if not isinstance(request.user, ProGofer):
            return Response({'error': 'Sorry, you do not have permission to view schedules.'}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(ProGofer, pk=request.user.pk)
        schedules = Schedule.objects.filter(gofer=user)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        message_poster = request.user
        pro_gofer = get_object_or_404(ProGofer, pk=request.data.get('gofer_id'))
        schedule = get_object_or_404(Schedule, pk=request.data.get('schedule_id'))
        duration = int(request.data.get('duration', 1))

        data = {
            'message_poster': message_poster.id,
            'pro_gofer': pro_gofer.id,
            'schedule': schedule.id,
            'duration': duration
        }

        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingListView(generics.ListAPIView):
    """List Bookings for a given progofer"""
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        if isinstance(self.request.user, MessagePoster):
            return Booking.objects.filter(message_poster=self.request.user)
        return Booking.objects.filter(pro_gofer=self.kwargs.get('pk'))


class BookingUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user, status='Pending')


class BookingCancelView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user, status='Pending')

    def perform_destroy(self, instance):
        instance.status = 'Terminated'
        instance.save()


class BookingAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=request.data.get('booking_id'))
        if booking.gofer.user == request.user:
            booking.status = 'Accepted'
            booking.save()
            return Response({'status': 'Booking accepted.'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to accept this booking.'}, status=status.HTTP_403_FORBIDDEN)


class BookingDeclineView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=request.data.get('booking_id'))
        comment = request.data.get('comment', '')
        if booking.gofer.user == request.user:
            booking.status = 'Declined'
            booking.comment = comment
            booking.save()
            return Response({'status': 'Booking declined.'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to decline this booking.'}, status=status.HTTP_403_FORBIDDEN)
