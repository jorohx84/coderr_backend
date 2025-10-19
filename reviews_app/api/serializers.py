from rest_framework import serializers
from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Notes:
    - The 'reviewer', 'created_at', and 'updated_at' fields are read-only and cannot be modified by the user.

    """
    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
            ]
        
        read_only_fields = ['reviewer', 'created_at', 'updated_at']