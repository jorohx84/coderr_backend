from rest_framework import serializers
from ..models import Profile

class ProfileSerializer(serializers.ModelSerializer):

    """
    General serializer for full user profile data.

    This serializer is typically used when retrieving or updating
    complete profile information for both business and customer users.

    """

    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)


    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'email', 'type',
            'first_name', 'last_name', 'file',
            'location', 'tel', 'description', 'working_hours',
            'created_at',
        ]

class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying business user profile data.

    This serializer is optimized for public views or listings of business profiles.
    It excludes private fields such as email and created_at for privacy and simplicity.

    """

    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)


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


    class Meta:
        model = Profile
        fields = [
            'user', 
            'username', 
            'first_name', 
            'last_name', 
            'file',
            'tel', 
            'type',
        ]


