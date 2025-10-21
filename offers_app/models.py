from django.db import models
from django.conf import settings

class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        created_str = self.created_at.strftime("%d.%m.%Y %H:%M")
        updated_str = self.updated_at.strftime("%d.%m.%Y %H:%M")
        return f"{created_str} - {self.title} created by {self.user.username} - last update: {updated_str}"


class OfferDetail(models.Model):
    TYPE_CHOICES = (
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    )

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=20, choices=TYPE_CHOICES)


    def __str__(self):
        return f"{self.offer.title} - {self.title}"


class Feature(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name