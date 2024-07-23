import re
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models import Q
from django.conf import settings
from rest_framework.decorators import action
from main.pagination import CustomPagination
from .models import Booking, CustomUser, Gofer, Media, ProGofer, Schedule
from main.models import MessagePoster
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from main.serializers import LocationSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import CreateAndDeleteBookingSerializer, GoferCreateSerializer, LoginUserSerializer, MediaSerializer, MessagePosterSerializer, ProGoferSerializer, ReadBookingSerializer, RegisterCustomUserSerializer, GoferSerializer, CustomUserSerializer, ScheduleSerializer, UpdateBookingSerializer
from . import utils
from .filters import GoferFilterSet
from .decorators import phone_unverified
from transaction.models import Wallet
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView


class RegisterUserView(ModelViewSet):
    ''' 
    Register new CustomUser
    
    This view expects user details in JSON format and returns a pair of
    JWT token(access and refresh) upon successful registration
    
    '''
    serializer_class = RegisterCustomUserSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ['post']
    def create(self, request):
        if request.user.is_authenticated:
            return Response({'detail': 'User already authenticated.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = RegisterCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            phone_number = user.phone_number
            return_message = dict()
            try:
                wallet = Wallet.objects.create(custom_user=user)
                wallet.save()
                message_poster = MessagePoster.objects.create(custom_user=user)
                message_poster.save()
                refresh = RefreshToken.for_user(user)
                return_message['refresh'] = str(refresh)
                return_message['access'] = str(refresh.access_token)
                return_message['auth_status'] = str(user.is_authenticated)
                return_message['email'] = str(user.email)
                return_message['phone_number'] = str(user.phone_number)
                #utils.send(phone_number)
                return Response(return_message, status=status.HTTP_201_CREATED)
            except Exception as e:
                return_message['error'] = str(e.__str__)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@phone_unverified
@permission_classes([IsAuthenticated])
def verify_phone(request):
    code = request.data.get('code')
    if utils.check(request.user.phone_number, code):
        request.user.phone_verified = True
        request.user.save()
        return Response({
            'detail': 'Phone number verified successfully.'
        }, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid or expired verification code.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_verification_email(request):
    '''
    Send a verification email to the user
    
    This view expects a JSON payload with the email address and 
    returns a HTTP 200 OK status upon successful email sending
    '''
    user = request.user
    if user.email_verified:
        return Response({"detail": "Email already verified."}, status=status.HTTP_400_BAD_REQUEST)
    if user.email == request.data['email']:
        # Generate verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = request.build_absolute_uri(
            reverse(viewname='verify_email', kwargs={'uidb64': uid, 'token': token})
        )
        try:
            # Send verification email
            send_mail(
                'Verify your email address',
                f'Click the link to verify your email address: {verification_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({"detail": "Email successfully sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        return Response({'detail': 'Email verified successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUserView(ModelViewSet):
    '''
    Login a user
    
    Accepts a JSON payload with the email/phone number and 
    returns a pair of JWT tokens(access and refresh) upon successful authentication
    '''
    queryset = CustomUser.objects.all()
    serializer_class = LoginUserSerializer
    http_method_names = ['post']
    
    def create(self, request):
        identifier = request.data.get('identifier')
        password = request.data.get('password')
        user = CustomUser.objects.filter(Q(email=identifier) | Q(phone_number=identifier)).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'auth_status': str(user.is_authenticated)
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout a user by blacklisting the refresh token.

    This view expects a JSON payload with the refresh token.
    It returns a HTTP 205 Reset Content status upon successful logout.

    Parameters:
    request (Request): The incoming request object containing the refresh token.

    Returns:
    Response: A HTTP response with the appropriate status and message.
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except KeyError:
        return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class GoferViewset(ModelViewSet):
    queryset = Gofer.objects.all()
    serializer_class = GoferSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GoferFilterSet
    search_fields = ['$bio', 'mobility_means', 'expertise']
    ordering_fields = ['mobility_means', 'charges', 'avg_rating']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return GoferCreateSerializer
        return GoferSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, pk):
        gofer = Gofer.objects.get(id=pk)
        serializer = GoferSerializer(data=request.data, instance=gofer, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def ToggleAvailability(request):
    try:
        gofer = Gofer.objects.get(id=request.user.gofer.id)
        gofer.is_available = gofer.toggle_availability()
        gofer.save()
        return Response(GoferSerializer(gofer).data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({'error': 'This user is not a Gofer'})
    
class CurrentUserView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class MediaViewset(ModelViewSet):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()
    def get_queryset(self):
        vendor_id = self.kwargs['vendor_pk']
        return Media.objects.filter(vendor__id=vendor_id)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    

class MessagePosterViewSet(ModelViewSet):
    queryset = MessagePoster.objects.select_related('custom_user').all()
    serializer_class = MessagePosterSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['custom_user__first_name']
    search_fields = ['custom_user__first_name']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        return {"currently_logged_in_user": self.request.user.id}
    
    
class ScheduleViewSet(ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Schedule.objects.select_related('pro_gofer').filter(pro_gofer_id=self.kwargs['pro_gofer_pk'])
    
    def get_serializer_context(self):
        return {'pro_gofer_id': self.kwargs['pro_gofer_pk']}
    
    
class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.select_related('pro_gofer').select_related('message_poster').all()
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadBookingSerializer
        elif self.request.method == 'PUT':
            return UpdateBookingSerializer
        return CreateAndDeleteBookingSerializer
    
    @action(detail=True, methods=['post'])
    def accept_booking(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        booking.status = 'accepted'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def decline_booking(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        booking.status = 'declined'
        booking.pro_gofer.save()
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)


class ProGoferViewSet(ModelViewSet):
    queryset = ProGofer.objects.select_related('custom_user').all()
    serializer_class = ProGoferSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['profession', 'hourly_rate', 'custom_user']
    search_fields = ['profession', 'hourly_rate', 'custom_user']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        currently_logged_in_user_id = self.request.user.id
        return {'currently_logged_in_user_id': currently_logged_in_user_id}
    
        
        
    
