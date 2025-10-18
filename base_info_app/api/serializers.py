from django.db.models import Avg
from rest_framework import serializers
from ..models import BaseInfo
from reviews_app.models import Review
from profile_app.models import Profile
from offers_app.models import Offer

class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    business_profile_count = serializers.SerializerMethodField()
    offer_count = serializers.SerializerMethodField()

    def get_review_count(self, obj):
        count = Review.objects.count()
        return count
    
    def get_average_rating(self, obj):
        avg = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if avg is None:
            return 0
        return round(avg, 1)
    
    def get_business_profile_count(self, obj):
        count = Profile.objects.filter(type='business').count()

        return count 

    def get_offer_count(self, obj):
        count =Offer.objects.count()
        return count