from django.db import models
from django.contrib.auth.models import User


class RareUser(models.Model):
    bio = models.CharField(max_length=200)
    profile_image_url = models.URLField(default=None)
    created_on = models.DateField(auto_now_add=True)
    active = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="rare_user_user")


