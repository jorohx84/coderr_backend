from rest_framework import serializers
from ..models import Profile
from auth_app.models import CustomUser
class ProfileSerializer(serializers.ModelSerializer):

    """
    General serializer for full user profile data.

    This serializer is typically used when retrieving or updating
    complete profile information for both business and customer users.

    """

    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    file = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Profile
        fields = [
            'user', 
            'username', 
            'email', 
            'type',
            'first_name', 
            'last_name', 
            'file',
            'location', 
            'tel', 
            'description', 
            'working_hours',
            'created_at',
        ]

    def update(self, instance, validated_data):
        email = validated_data.pop('email')
        print(email)
        if email:
            user = instance.user
            if user.email != email:
                user.email = email
                user.save()
        instance.email = email

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.save()
        return instance



class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying business user profile data.

    This serializer is optimized for public views or listings of business profiles.
    It excludes private fields such as email and created_at for privacy and simplicity.

    """

    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    file = serializers.ImageField(required=False, allow_null=True)
   

    class Meta:
        model = Profile
        fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'location', 
            'tel', 
            'description', 
            'working_hours',
            'type',
        ]



class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying customer user profile data.

    This serializer is optimized for public or limited views of customer profiles,
    typically omitting detailed or sensitive information.

    """

    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    file = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'type',
        ]


