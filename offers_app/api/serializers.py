
from django.db import models
from rest_framework import serializers
from ..models import Offer, OfferDetails, Feature
from profile_app.models import Profile


class FeatureSerializer(serializers.StringRelatedField):
    def to_internal_value(self, data):
        feature, _ = Feature.objects.get_or_create(name=data)
        return feature


class OfferDetailsSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)

    class Meta:
        model = OfferDetails
        fields = [
            "id", "title", "revisions", "delivery_time_in_days", "price",
            "features", "offer_type"
        ]


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user=self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)

        for detail_data in details_data:
            features = detail_data.pop('features')
            detail = OfferDetails.objects.create(offer=offer, **detail_data)
            detail.features.set(features)

        return offer







class OfferDetailsShortSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetails
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username']

class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailsShortSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time',
            'user_details'
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(models.Min('price'))['price__min'] or 0

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0
