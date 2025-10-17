
# from django.db import models
# from rest_framework import serializers
# from ..models import Offer, OfferDetails, Feature
# from profile_app.models import Profile


# class FeatureSerializer(serializers.StringRelatedField):
#     def to_internal_value(self, data):
#         feature, _ = Feature.objects.get_or_create(name=data)
#         return feature


# class OfferDetailsSerializer(serializers.ModelSerializer):
#     features = FeatureSerializer(many=True)

#     class Meta:
#         model = OfferDetails
#         fields = [
#             "id", "title", "revisions", "delivery_time_in_days", "price",
#             "features", "offer_type"
#         ]
  

# class OfferSerializer(serializers.ModelSerializer):
#     details = OfferDetailsSerializer(many=True)

#     class Meta:
#         model = Offer
#         fields = ["id", "title", "image", "description", "details"]

#     def to_representation(self, instance):  
#         rep = super().to_representation(instance)
#         print("Serialized Offer Data:", rep)  # Debug-Ausgabe in der Konsole
#         return rep
#     def create(self, validated_data):
#         details_data = validated_data.pop('details')
#         if len(details_data) < 3:
#             raise serializers.ValidationError({"error": "An offer must contain at least 3 offer packages (details)."})
#         user=self.context['request'].user
#         offer = Offer.objects.create(user=user, **validated_data)

#         for detail_data in details_data:
#             features = detail_data.pop('features')
#             detail = OfferDetails.objects.create(offer=offer, **detail_data)
#             detail.features.set(features)

#         return offer
    


# class OfferDetailsShortSerializer(serializers.ModelSerializer):
#     url = serializers.SerializerMethodField()

#     class Meta:
#         model = OfferDetails
#         fields = ['id', 'url']

#     def get_url(self, obj):
#         return f"/offerdetails/{obj.id}/"

# class UserDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['first_name', 'last_name', 'username']

# class OfferListSerializer(serializers.ModelSerializer):
#     details = OfferDetailsShortSerializer(many=True, read_only=True)
#     min_price = serializers.SerializerMethodField()
#     min_delivery_time = serializers.SerializerMethodField()
#     user_details = UserDetailsSerializer(source='user.profile', read_only=True)

#     class Meta:
#         model = Offer
#         fields = [
#             'id', 
#             'user', 
#             'title', 
#             'image', 
#             'description',
#             'created_at', 
#             'updated_at',
#             'details', 
#             'min_price', 
#             'min_delivery_time',
#             'user_details'
#         ]

#     def get_min_price(self, obj):
#         return obj.details.aggregate(models.Min('price'))['price__min'] or 0

#     def get_min_delivery_time(self, obj):
#         return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0




# class SinglerOfferSerializer(serializers.ModelSerializer):
#     details = OfferDetailsShortSerializer(many=True, read_only=True)
#     min_price = serializers.SerializerMethodField()
#     min_delivery_time = serializers.SerializerMethodField() 

#     class Meta:
#         model = Offer
#         fields = [
#             'id', 
#             'user', 
#             'title', 
#             'image', 
#             'description',
#             'created_at', 
#             'updated_at',
#             'details', 
#             'min_price', 
#             'min_delivery_time'
#         ]

#     def get_min_price(self, obj):
#         return obj.details.aggregate(models.Min('price'))['price__min'] or 0

#     def get_min_delivery_time(self, obj):
#         return obj.details.aggregate(models.Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0


# serializers.py

from rest_framework import serializers
from ..models import Offer, OfferDetail, Feature
from django.contrib.auth import get_user_model

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details', 'created_at', 'updated_at']

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Ein Angebot muss genau 3 Details enthalten.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer





User = get_user_model()

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

class OfferDetailURLSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailURLSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserSummarySerializer(source="user", read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description",
            "created_at", "updated_at", "details",
            "min_price", "min_delivery_time", "user_details"
        ]

    def get_min_price(self, obj):
        details = obj.details.all()
        prices = [detail.price for detail in details if detail.price is not None]
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        delivery_times = [detail.delivery_time_in_days for detail in details if detail.delivery_time_in_days is not None]
        return min(delivery_times) if delivery_times else None


class SingleOfferSerializer(serializers.ModelSerializer):
    details = OfferDetailURLSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    

    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description",
            "created_at", "updated_at", "details",
            "min_price", "min_delivery_time"
        ]

    def get_min_price(self, obj):
        details = obj.details.all()
        prices = [detail.price for detail in details if detail.price is not None]
        return min(prices) if prices else None

    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        delivery_times = [detail.delivery_time_in_days for detail in details if detail.delivery_time_in_days is not None]
        return min(delivery_times) if delivery_times else None





class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        exclude = ['offer']  # Da die Offer-ID automatisch vom Parent kommt

# class OfferUpdateSerializer(serializers.ModelSerializer):
#     details = OfferDetailUpdateSerializer(many=True, required=False)

#     class Meta:
#         model = Offer
#         fields = ['title', 'image', 'description', 'details']

#     def update(self, instance, validated_data):
#         # Update einfache Felder (title, image, description)
#         for attr, value in validated_data.items():
#             if attr != 'details':
#                 setattr(instance, attr, value)

#         instance.save()

#         # Update der Details (optional, wenn im Request enthalten)
#         details_data = validated_data.get('details')
#         if details_data:
#             # Mapping bestehender Details nach `offer_type`
#             existing_details = {d.offer_type: d for d in instance.details.all()}
            
#             for detail_data in details_data:
#                 offer_type = detail_data.get('offer_type')
#                 if offer_type in existing_details:
#                     detail_instance = existing_details[offer_type]
#                     for attr, value in detail_data.items():
#                         setattr(detail_instance, attr, value)
#                     detail_instance.save()
#                 else:
#                     # Optional: Detail neu anlegen, falls nicht vorhanden
#                     OfferDetail.objects.create(offer=instance, **detail_data)

#         return instance

class OfferUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        # 1. Normale Felder aktualisieren
        for attr, value in validated_data.items():
            if attr != 'details':
                setattr(instance, attr, value)
        instance.save()

        # 2. Details aktualisieren
        details_data = validated_data.get('details')
        if details_data is not None:
            existing_details = {d.offer_type: d for d in instance.details.all()}

            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if not offer_type:
                    continue  # oder raise serializers.ValidationError("offer_type erforderlich")

                detail_instance = existing_details.get(offer_type)
                if detail_instance:
                    # update
                    for attr, value in detail_data.items():
                        setattr(detail_instance, attr, value)
                    detail_instance.save()
                else:
                    # create
                    OfferDetail.objects.create(offer=instance, **detail_data)

        return instance

class FeatureSerializer(serializers.StringRelatedField):
    def to_internal_value(self, data):
        feature, _ = Feature.objects.get_or_create(name=data)
        return feature