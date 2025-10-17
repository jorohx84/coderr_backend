from django.db import models
from django.conf import settings
from offers_app.models import Offer, OfferDetail, Feature

class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In_Progress'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    ]
    customer_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_orders')
    business_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business_orders')
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.PROTECT, related_name='orders')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.CharField(max_length=50, choices=OfferDetail.TYPE_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    features = models.ManyToManyField(Feature, related_name='orders')

