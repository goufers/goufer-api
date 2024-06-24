import re
from rest_framework import serializers
from .models import CustomUser, Gofer, Vendor, ErrandBoy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from main.serializers import GoferDocumentSerializer, ErrandBoyDocumentSerializer, VendorDocumentSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    '''
    Serializer for custom users

    This serializer is used to create and update custom user instances.

    Attributes:
        model (CustomUser): The model this serializer is based on.
        fields (list): A list of fields to include in the serializer.
        extra_kwargs (dict): Additional keyword arguments to pass to the underlying model's create_user method.

    Methods:
        create(validated_data):
        This method is used to create a new custom user instance. It takes the validated data as input and returns the newly created user instance.

    Args:
        validated_data (dict): A dictionary containing the validated data for the new user instance.

    Returns:
        CustomUser: A newly created custom user instance.
    '''
    
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return password
    
    def validate_phone_number(self, phone_number):
        if len(phone_number)!= 14:
            raise serializers.ValidationError("Enter valid phone number")
        elif not phone_number.startswith('+'):
            raise serializers.ValidationError("Phone number must include country code starting with +")
        return phone_number
    
    def create(self, validated_data):
        '''
        This method is used to create a new custom user instance. It takes the validated data as input and returns the newly created user instance.

        Args:
            validated_data (dict): A dictionary containing the validated data for the new user instance.

        Returns:
            CustomUser: A newly created custom user instance.
        '''
        self.validate_password(validated_data['password'])
        user = CustomUser.objects.create_user(
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
    

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'gender', 'first_name', 'last_name', 'location'
        ]
        
        


class GoferSerializer(serializers.ModelSerializer):
    documents = GoferDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Gofer
        fields = "__all__"
        
class VendorSerializer(serializers.ModelSerializer):
    documents = VendorDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Vendor
        fields = "__all__"
        
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self, request):
        user = CustomUser.objects.get(email=self.validated_data['email'])
        uid = urlsafe_base64_encode(str(user.pk).encode())
        token = default_token_generator.make_token(user)
        password_reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uid': uid, 'token': token}))
        subject = "Password Reset Request"
        context = {
            "user": user,
            "reset_link": password_reset_url
        }
        message = render_to_string("user/password_reset_email.html", context=context)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(message, "text/html")
        email.send()

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)


class ErrandBoySerializer(serializers.ModelSerializer):
    documents = ErrandBoyDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = ErrandBoy
        fields = "__all__"
