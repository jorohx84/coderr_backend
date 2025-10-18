from django.db import models

class BaseInfo(models.Model):
    review_count = models.IntegerField()
    average_rating = models.IntegerField()
    business_profile_count = models.IntegerField()
    offer_count = models.IntegerField()
