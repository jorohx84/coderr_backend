from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from ..models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
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