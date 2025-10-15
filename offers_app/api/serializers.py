from rest_framework import serializers
from ..models import Offer, OfferDetails, Feature

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


