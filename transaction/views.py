# views.py

from rest_framework import generics, status
from rest_framework.decorators import action
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
from rest_framework.viewsets import ModelViewSet
from user.models import CustomUser, Gofer
from django.db.models import Count


paystack_secret_key = 'sk_test_58d7c6da2b1b3fb1c246d71e090cc18d76221624'


class FundWalletView(APIView):
    """Fund user wallet."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = FundWalletSerializer(data=request.data)
        if serializer.is_valid():
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
        # print(response_data)
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
        transactions = Transaction.objects.filter(wallet__user=request.user).order_by('-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScheduleViewSet(ModelViewSet):
    """ViewSet for managing schedules"""
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.user_type == 'ProGofer':
            return Schedule.objects.none()
        user = get_object_or_404(ProGofer, custom_user=self.request.user)
        return Schedule.objects.filter(pro_gofer=user)

    def perform_create(self, serializer):
        user = get_object_or_404(ProGofer, custom_user=self.request.user)
        serializer.save(pro_gofer=user)
    
    def perform_update(self, serializer):
        user = get_object_or_404(ProGofer, custom_user=self.request.user)
        serializer.save(pro_gofer=user)


class BookingViewSet(ModelViewSet):
    # queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.request.user.pk)

        if user.user_type == 'MessagePoster':
            return Booking.objects.filter(message_poster=user)
        elif user.user_type == 'ProGofer':
            pro_gofer = get_object_or_404(ProGofer, custom_user=user)
            return Booking.objects.filter(pro_gofer=pro_gofer)
        return Booking.objects.none()

    def perform_create(self, serializer):
        message_poster = get_object_or_404(MessagePoster, pk=self.request.data.get('message_poster'))
        pro_gofer = get_object_or_404(ProGofer, pk=self.request.data.get('pro_gofer'))
        schedule = get_object_or_404(Schedule, pk=self.request.data.get('schedule').get('id'))
        print(schedule)
        duration = int(self.request.data.get('duration')) if self.request.data['duration'] else 1
        serializer.save(message_poster=message_poster, pro_gofer=pro_gofer, schedule=schedule, duration=duration)

    def perform_update(self, serializer):
        user = self.request.user
        if user.user_type == 'ProGofer':
            pro_gofer = get_object_or_404(ProGofer, custom_user=user)
            serializer.save(pro_gofer=pro_gofer)
        else:
            serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def accept(self, request, pk=None):
        """Accept a user's booking"""
        booking = get_object_or_404(Booking, pk=pk)
        if booking.pro_gofer.custom_user == request.user:
            booking.status = 'Active'
            booking.save()
            return Response({'status': 'Booking accepted.'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to accept this booking.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def decline(self, request, pk=None):
        """decline a booking"""
        booking = get_object_or_404(Booking, pk=pk)
        pro_gofer = get_object_or_404(ProGofer, custom_user=booking.pro_gofer.custom_user)
        comment = request.data.get('comment', '')
        if booking.pro_gofer.custom_user == request.user:
            booking.status = 'Declined'
            booking.comment = comment
            booking.save()
            pro_gofer.maximum_bookings += 1
            pro_gofer.save()
            return Response({'status': 'Booking declined.'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to decline this booking.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        """Terminate a booking"""
        booking = get_object_or_404(Booking, pk=pk)
        pro_gofer = get_object_or_404(ProGofer, custom_user=booking.pro_gofer.custom_user)
        if booking.message_poster == request.user and booking.status == 'Pending Approval':
            booking.status = 'Cancelled'
            booking.save()
            pro_gofer.maximum_bookings += 1
            return Response({'status': 'Booking canceled.'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to cancel this booking.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def initiate_termination(self, request, pk=None):
        """ Initiate termination for a previously accepted booking"""
        booking = get_object_or_404(Booking, pk=pk)
        comment = request.data.get('comment', '')
        if booking.pro_gofer.custom_user == request.user and booking.status == 'Active':
            booking.status = 'Pending Termination'
            booking.comment = comment
            booking.save()
            return Response({'status': f'Termination approval sent to {booking.message_poster.custom_user.first_name}'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to reject this booking.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve_termination(self, request, pk=None):
        """Terminate a booking"""
        booking = get_object_or_404(Booking, pk=pk)
        pro_gofer = get_object_or_404(ProGofer, custom_user=booking.pro_gofer.custom_user)
        if booking.message_poster == request.user and booking.status == 'Pending Termination':
            booking.status = 'Terminated'
            booking.save()
            pro_gofer.maximum_bookings += 1
            pro_gofer.save()
            return Response({'status': 'Booking terminated.'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to terminate this booking.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def settle(self, request, pk=None):
        """Indicates that the booking has been successfully settled"""
        booking = get_object_or_404(Booking, pk=pk)
        pro_gofer = get_object_or_404(ProGofer, custom_user=booking.pro_gofer.custom_user)
        if booking.pro_gofer.custom_user == request.user or booking.message_poster == request.user:
            booking.status = 'Settled'
            booking.save()
            pro_gofer.maximum_bookings += 1
            return Response({'status': 'Booking settled.'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not authorized to settle this booking.'}, status=status.HTTP_403_FORBIDDEN)
