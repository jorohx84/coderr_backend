from rest_framework import serializers
from ..models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """

    Serializer for the Review model.

    Function:
    - Handles serialization and deserialization of Review instances.
    - Automatically sets fields like 'reviewer', 'created_at', and 'updated_at' as read-only.

    Validation:
    - On creation (POST), it checks whether the currently authenticated user (reviewer)
      has already submitted a review for the same business user (business_user).
    - If such a review already exists, a validation error is raised to prevent duplicate reviews.

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

    def validate(self, data):
        request = self.context.get('request')
        reviewer = request.user
        business_user = data.get('business_user')

        if self.instance is None:
            already_exists = Review.objects.filter(reviewer=reviewer, business_user=business_user).exists()

            if already_exists:
                raise serializers.ValidationError("you have already left a review for this business user.")
        
        return data