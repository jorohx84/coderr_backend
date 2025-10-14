from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from ..models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Fields:
    - fullname: full name of the user (write-only)
    - email: user's email address
    - password: user's password (write-only)
    - repeated_password: confirmation of the password (write-only)

    Validates:
    - Email must be unique.
    - Password and repeated_password must match.

    On creation:
    - Creates a new User instance with username set to email.
    - Sets the password securely.
    - Creates a related UserProfile instance.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username","email", "password", "repeated_password", "type"]
        read_only_fields = ["id"]
    
    def validate(self, attrs):
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "User with this email already excist"})
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError({"repeated_password": "Password do not match"})
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('repeated_password')

        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
    

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Fields:
    - email: user's email address
    - password: user's password (write-only)

    Validates:
    - Checks if the provided email and password authenticate a user.
    """
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Invalid username or password"})
        attrs["user"] = user
        return attrs