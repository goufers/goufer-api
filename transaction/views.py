# views.py
from pprint import pprint
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly 
from django.shortcuts import get_object_or_404
from .models import Wallet, Transaction, Bank, ProGofer, MessagePoster
from .serializers import BankSerializer, FundWalletSerializer, TransferFundsSerializer, TransactionSerializer 
from .models import (
    StripeUser, Wallet, Transaction, Bank, ProGofer, MessagePoster
    )

from .serializers import (
    BankSerializer, 
    FundWalletSerializer, TransferFundsSerializer,
    TransactionSerializer
    )
import requests
from decimal import Decimal
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import viewsets
from user.models import Booking, CustomUser, Gofer, Schedule
from django.db.models import Count
import stripe
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

stripe.api_key = "sk_test_51PcjKqLFE9BMR2wqWSRB8YJ50qPQoe5lBQTwdqh8LE3vGF48a4aUwzgFQuKrZm255fmPG8exI3IG3KlrxYNa9VTh00g49Ra9B9"


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



# class BookingCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         message_poster = request.user
#         pro_gofer = get_object_or_404(ProGofer, pk=request.data.get('gofer_id'))
#         schedule = get_object_or_404(Schedule, pk=request.data.get('schedule_id'))
#         duration = int(request.data.get('duration', 1))

#         data = {
#             'message_poster': message_poster.id,
#             'pro_gofer': pro_gofer.id,
#             'schedule': schedule.id,
#             'duration': duration
#         }

#         serializer = BookingSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BookingListView(generics.ListAPIView):
#     """List Bookings for a given progofer"""
#     permission_classes = [IsAuthenticated]
#     serializer_class = BookingSerializer

#     def get_queryset(self):
#         if isinstance(self.request.user, MessagePoster):
#             return Booking.objects.filter(message_poster=self.request.user)
#         return Booking.objects.filter(pro_gofer=self.kwargs.get('pk'))


# class BookingUpdateView(generics.UpdateAPIView):
#     queryset = Booking.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Booking.objects.filter(user=self.request.user, status='Pending')


# class BookingCancelView(generics.DestroyAPIView):
#     queryset = Booking.objects.all()
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Booking.objects.filter(user=self.request.user, status='Pending')

#     def perform_destroy(self, instance):
#         instance.status = 'Terminated'
#         instance.save()


# class BookingAcceptView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         booking = get_object_or_404(Booking, pk=request.data.get('booking_id'))
#         if booking.gofer.user == request.user:
#             booking.status = 'Accepted'
#             booking.save()
#             return Response({'status': 'Booking accepted.'}, status=status.HTTP_200_OK)
#         return Response({'error': 'You are not authorized to accept this booking.'}, status=status.HTTP_403_FORBIDDEN)


# class BookingDeclineView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         booking = get_object_or_404(Booking, pk=request.data.get('booking_id'))
#         comment = request.data.get('comment', '')
#         if booking.gofer.user == request.user:
#             booking.status = 'Declined'
#             booking.comment = comment
#             booking.save()
#             return Response({'status': 'Booking declined.'}, status=status.HTTP_200_OK)
#         return Response({'error': 'You are not authorized to decline this booking.'}, status=status.HTTP_403_FORBIDDEN)

class CreatePaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            amount = request.data.get('amount')
            currency = request.data.get('currency')
            stripe_user = StripeUser.objects.get(user=user)
            if stripe_user.stripe_id is None:
                customer = stripe.Customer.create(
                    name=user.get_full_name(),
                    email=user.email,
                    phone=user.phone_number,
                    balance=int(Wallet.objects.get(custom_user=user).balance)
                )
                stripe_user.stripe_id = customer.get('id')
                stripe_user.save()
            else:
                customer = stripe.Customer.retrieve(stripe_user.stripe_id)
            intent = stripe.PaymentIntent.create(
                customer=user.stripe_user.stripe_id,
                amount=int(float(amount) * 100),
                currency=currency,
                automatic_payment_methods={
                    'enabled': True
                    },
                metadata={'user_id': user.id}
            )
            return Response({'payment_intent_id': intent}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ConfirmPaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            payment_intent_id = request.data.get('payment_intent_id')
            payment_intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                payment_method=request.data.get('payment_method_id'),
                return_url=request.build_absolute_uri(reverse("fund_wallet")),
                receipt_email=request.user.email
            )
            if payment_intent.status == 'succeeded':
                user = request.user
                wallet = Wallet.objects.get(custom_user=user)
                amount = payment_intent.amount / 100  # Convert cents to dollars
                wallet.balance += Decimal(amount)
                wallet.save()

                return Response({'message': 'Payment succeeded', 'balance': wallet.balance}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment not successful'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        user_id = payment_intent['metadata']['user_id']
        amount = payment_intent['amount_received'] / 100  # Convert cents to dollars

        user = CustomUser.objects.get(id=user_id)
        wallet = Wallet.objects.get(user=user)
        wallet.balance += amount
        wallet.save()

    return JsonResponse({'status': 'success'}, status=200)

