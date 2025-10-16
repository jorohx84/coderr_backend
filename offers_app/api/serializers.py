
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
        if len(details_data) < 3:
            raise serializers.ValidationError({"error": "An offer must contain at least 3 offer packages (details)."})
        user=self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)

        for detail_data in details_data:
            features = detail_data.pop('features')
            detail = OfferDetails.objects.create(offer=offer, **detail_data)
            detail.features.set(features)

        return offer
    

    # def update(self, instance, validated_data):
    #     details_data = validated_data.pop('details', None)

    # # Update der Felder des Offers
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()

    #     if details_data is not None:
    #         existing_details = {detail.id: detail for detail in instance.details.all()}
    #         sent_detail_ids = []

    #         for detail_data in details_data:
    #             features_data = detail_data.pop('features', [])
    #             detail_id = detail_data.get('id')

    #             if detail_id and detail_id in existing_details:
    #                 # Detail aktualisieren
    #                 detail_instance = existing_details[detail_id]
    #                 for attr, value in detail_data.items():
    #                     setattr(detail_instance, attr, value)
    #                 detail_instance.save()
    #                 detail_instance.features.set(features_data)
    #                 sent_detail_ids.append(detail_id)
    #             else:
    #                 # Neues Detail anlegen (ID fehlt oder nicht bekannt)
    #                 new_detail = OfferDetails.objects.create(offer=instance, **detail_data)
    #                 new_detail.features.set(features_data)
    #                 sent_detail_ids.append(new_detail.id)

    #         # Nicht mehr gesendete Details löschen
    #         for detail_id, detail in existing_details.items():
    #             if detail_id not in sent_detail_ids:
    #                 detail.delete()

    #         return instance
    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        offer = super().update(instance, validated_data)


        existing_details = {detail.id: detail for detail in offer.details.all()}

        for detail_data in details_data:
            detail_id = detail_data.get("id")
            if not detail_id:
                continue  

            detail_instance = existing_details.get(detail_id)
            if not detail_instance:
                continue  

       
            features = detail_data.pop("features", None)

       
            for field in ["price", "revisions", "delivery_time_in_days"]:
                if field in detail_data:
                    raw_value = detail_data[field]
                    if raw_value != "" and raw_value is not None:
                        try:
                            if field == "price":
                                detail_data[field] = float(raw_value)
                            else:
                                detail_data[field] = int(raw_value)
                        except (ValueError, TypeError):
                            raise serializers.ValidationError(
                            {field: f"Ungültiger Wert für '{field}': {raw_value}"}
                        )

    
            for attr, value in detail_data.items():
                setattr(detail_instance, attr, value)

            detail_instance.save()

            if features is not None:
                detail_instance.features.set(features)

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
            'id', 
            'user', 
            'title', 
            'image', 
            'description',
            'created_at', 
            'updated_at',
            'details', 
            'min_price', 
            'min_delivery_time',
            'user_details'
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(models.Min('price'))['price__min'] or 0

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0




class SinglerOfferSerializer(serializers.ModelSerializer):
    details = OfferDetailsShortSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField() 

    class Meta:
        model = Offer
        fields = [
            'id', 
            'user', 
            'title', 
            'image', 
            'description',
            'created_at', 
            'updated_at',
            'details', 
            'min_price', 
            'min_delivery_time'
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(models.Min('price'))['price__min'] or 0

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0