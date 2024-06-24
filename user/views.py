from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models import Q
from goufer import settings
from .models import CustomUser, Gofer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from main.serializers import LocationSerializer
from .serializers import CustomUserSerializer, UpdateProfileSerializer, GoferSerializer
from . import utils
from .decorators import phone_verification_required, phone_unverified
from transaction.models import Wallet
from django_filters.rest_framework import DjangoFilterBackend


@api_view(['POST'])
def register_user(request):
    ''' 
    Register new CustomUser
    
    This view expects user details in JSON format and returns a pair of
    JWT token(access and refresh) upon successful registration
    
    '''
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        wallet = Wallet.objects.create(user=user)
        wallet.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'auth_status': str(user.is_authenticated)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@phone_unverified
def send_code(request):
    phone_number = request.data.get('phone_number')
    try:
        utils.send(phone_number)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'detail': 'Verification code sent successfully.'}, status=status.HTTP_200_OK)

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
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return Response({"detail": "Email successfully sent"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
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
    
@api_view(['POST'])
def login_user(request):
    '''
    Login a user
    
    Accepts a JSON payload with the email/phone number and 
    returns a pair of JWT tokens(access and refresh) upon successful authentication
    '''
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

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@phone_verification_required
def UpdateProfile(request):
    user = CustomUser.objects.get(id=request.user.id)
    
    # Extract the location data from the request
    location_data = request.data.pop('location', None)

    # Update the user's profile information
    updated_user = UpdateProfileSerializer(instance=user, data=request.data, partial=True)

    if updated_user.is_valid():
        user = updated_user.save()
        
        if location_data:
            location_serializer = LocationSerializer(instance=user.location, data=location_data, partial=True)
            if location_serializer.is_valid():
                location_serializer.save()
            else:
                return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(updated_user.data, status=status.HTTP_200_OK)
    
    return Response(updated_user.errors, status=status.HTTP_400_BAD_REQUEST)

class GoferViewset(ModelViewSet):
    queryset = Gofer.objects.all()
    serializer_class = GoferSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    
    def update(self, request, pk):
        gofer = Gofer.objects.get(id=pk)
        serializer = GoferSerializer(data=request.data, instance=gofer, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
