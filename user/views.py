from django.shortcuts import render, redirect
from .models import CustomUser, Gofer, Vendor
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomUserSerializer, GoferSerializer, TokenPairSerializer
from transaction.serializers import Wallet # WalletSerializer, TransactionSerializer, Transaction



class TokenObtainPair(TokenObtainPairView):
    serializer_class = TokenPairSerializer

def authenticate_user(identifier, password):
    try:
        user = CustomUser.objects.get(Q(email=identifier) | Q(phone_number=identifier))
        if user.check_password(password):
            return user
    except CustomUser.DoesNotExist:
        return None
    return None


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
        refresh = RefreshToken.for_user(user=user)
        return Response(
            {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    '''
    Login a user
    
    Accepsts a JSON payload with the email/phone number and 
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
    


"""Wallet integration at signup"""
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
        refresh = RefreshToken.for_user(user=user)
        return Response(
            {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
