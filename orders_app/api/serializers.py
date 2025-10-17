from rest_framework import serializers
from ..models import Order
from offers_app.api.serializers import FeatureSerializer

class OrderSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)
 
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

