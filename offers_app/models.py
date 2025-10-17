# from django.db import models
# from django.conf import settings
# from django.utils import timezone

# class Offer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
#     title = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='offers/', null=True, blank=True)
#     description = models.TextField(default="")
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         if self.pk:
#             self.updated_at = timezone.now()
#         super().save(*args, **kwargs)


#     def __str__(self):
#         return self.title


# class Feature(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name
    


# class OfferDetails(models.Model):
#     TYPE_CHOICES = (
#         ('basic', 'Basic'),
#         ('standard', 'Standard'),
#         ('premium', 'Premium'),
#     )

#     offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     revisions = models.IntegerField()
#     delivery_time_in_days = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     features = models.ManyToManyField(Feature)
#     offer_type = models.CharField(max_length=50, choices=TYPE_CHOICES)


#     def __str__(self):
#         return f"{self.offer.title} - {self.title} ({self.offer_type})"



# models.py

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
        return self.title


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