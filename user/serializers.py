import re
from rest_framework import serializers

from main.models import Address, Reviews
from .models import Booking, CustomUser, Gofer, MessagePoster, Schedule, Vendor, ErrandBoy, ProGofer, Media
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from main.serializers import (
    DocumentSerializer, AddressSerializer, ReviewsSerializer, LocationSerializer, SubCategorySerializer
)
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q


class RegisterCustomUserSerializer(serializers.ModelSerializer):
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
    
class LoginUserSerializer(serializers.ModelSerializer):
    '''
    Serializer for user login
    '''
    identifier = serializers.CharField(max_length=100)
    class Meta:
        model = CustomUser
        fields = ['identifier', 'password']
    
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['vendor', 'media']
        read_only_fields = ['vendor']
    def create(self, validated_data):
        vendor = self.context['request'].user.vendor
        return Media.objects.create(vendor=vendor, media=validated_data['media'])
        
class CustomUserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    location = LocationSerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name', 'gender', 'location', 'address', 'documents', 'date_joined', 'phone_verified', 'email_verified']
        read_only_fields = ['phone_verified', 'email_verified', 'email', 'phone_number', 'email', 'date_joined']  

class GoferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gofer
        fields = ['expertise', 'mobility_means', 'bio', 'sub_category', 'charges', 'is_available']

    def create(self, validated_data):
        custom_user = self.context['request'].user
        gofer = Gofer.objects.create(custom_user=custom_user, **validated_data)
        return gofer

class GoferSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer()
    gofer_reviews = ReviewsSerializer(many=True, read_only=True)
    class Meta:
        model = Gofer
        fields = ['custom_user', 'expertise', 'mobility_means', 'bio', 'sub_category', 'charges', 'gofer_reviews']
        
    def update(self, instance, validated_data):
        custom_user_data = validated_data.pop('custom_user')
        custom_user = instance.custom_user
        address = instance.custom_user.address

        instance.expertise = validated_data.get('expertise', instance.expertise)
        instance.mobility_means = validated_data.get('mobility_means', instance.mobility_means)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.sub_category = validated_data.get('sub_category', instance.sub_category)
        instance.charges = validated_data.get('charges', instance.charges)
        instance.save()

        custom_user.email = custom_user_data.get('email', custom_user.email)
        custom_user.phone_number = custom_user_data.get('phone_number', custom_user.phone_number)
        custom_user.first_name = custom_user_data.get('first_name', custom_user.first_name)
        custom_user.last_name = custom_user_data.get('last_name', custom_user.last_name)
        custom_user.gender = custom_user_data.get('gender', custom_user.gender)
        custom_user.location = custom_user_data.get('location', custom_user.location)
        address_data = custom_user_data.get('address', custom_user.address)
        print(address)
        print(address_data)
        print(custom_user.address)
        address.house_number = address_data['house_number']
        address.street = address_data['street']
        address.city = address_data['city']
        address.state = address_data['state']
        address.country = address_data['country']
        address.save()
        custom_user.save()

        return instance
    
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'day_of_week_available', 'start_time_available', 'end_time_available']
        
    def create(self, validated_data):
        user_id = self.context['pro_gofer_id']
        return Schedule.objects.create(pro_gofer_id=user_id, **validated_data)


class MiniProGoferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProGofer
        fields = ['id', 'profession', 'hourly_rate', 'is_available']
        

class ReadBookingSerializer(serializers.ModelSerializer):
    pro_gofer = MiniProGoferSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ['id', 'scheduled_date', 'from_time', 'to_time', 'purpose', 'status', 'message_poster', 'pro_gofer']
        


class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['scheduled_date', 'from_time', 'to_time', 'purpose'] 
 
 
class CreateAndDeleteBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        
    
class ProGoferSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    bookings = ReadBookingSerializer(many=True, read_only=True)
    class Meta:
        model = ProGofer
        fields = ['id', 'custom_user', 'bio', 'profession', 'hourly_rate', 'is_available', 'schedules', 'bookings']
    
    def create(self, validated_data):
        user_id = self.context['currently_logged_in_user_id']
        return ProGofer.objects.create(custom_user_id=user_id, **validated_data)

class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'business_name', 'website', 'bio', 'facebook', 'twitter',
            'instagram', 'linkedin', 'category'
        ]
    def create(self, validated_data):
        custom_user = self.context['request'].user
        vendor = Vendor.objects.create(custom_user=custom_user, **validated_data)
        return vendor
        
class VendorSerializer(serializers.ModelSerializer):
    vendor_media = MediaSerializer(many=True, read_only=True)
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
        message = render_to_string("password_reset_email.html", context=context)
        
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
    class Meta:
        model = ErrandBoy
        fields = "__all__"
        
        

class MessagePosterSerializer(serializers.ModelSerializer):
    custom_user = CustomUserSerializer(read_only=True)
    class Meta:
        model = MessagePoster
        fields = ['id', 'custom_user']
        
    def create(self, validated_data):
        currently_logged_in_user_id = self.context["currently_logged_in_user"]
        return MessagePoster.objects.create(custom_user_id=currently_logged_in_user_id)
    
    

        
        
    


        
