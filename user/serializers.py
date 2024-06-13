from rest_framework import serializers
from .models import CustomUser, Gofer, Vendor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

    def create(self, validated_data):
        '''
        This method is used to create a new custom user instance. It takes the validated data as input and returns the newly created user instance.

        Args:
            validated_data (dict): A dictionary containing the validated data for the new user instance.

        Returns:
            CustomUser: A newly created custom user instance.
        '''
        user = CustomUser.objects.create_user(
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class TokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token

class GoferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gofer
        fields = "__all__"
