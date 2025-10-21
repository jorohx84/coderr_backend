from django.db import models
from auth_app.models import CustomUser
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=255, blank=True, default="")
    first_name = models.CharField(max_length=255, blank=True, default="")
    last_name = models.CharField(max_length=255, blank=True, default="")
    file = models.CharField(max_length=255, blank=True, null=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(max_length=50, blank=True, default="")
    working_hours = models.CharField(max_length=50, blank=True, default="")
    type = models.CharField()
    email = models.EmailField(max_length=50, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return f"{self.user.username}"
