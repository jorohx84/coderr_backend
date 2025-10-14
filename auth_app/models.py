from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )
   
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
