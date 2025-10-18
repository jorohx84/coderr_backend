from rest_framework import serializers
from ..models import Offer, OfferDetail, Feature
from profile_app.models import Profile



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


class UserSummarySerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="profile.first_name", read_only=True)
    last_name = serializers.CharField(source="profile.last_name", read_only=True)
    username = serializers.CharField(source="profile.username", read_only=True)

    class Meta:
        model = Profile
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