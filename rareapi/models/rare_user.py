from django.db import models
from django.contrib.auth.models import User


class RareUser(models.Model):
    bio = models.CharField(max_length=200)
    profile_image_url = models.URLField(default=None)
    created_on = models.DateField(auto_now_add=True)
    active = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="rare_user_user")


    @property
    def is_followed(self):
        return self.__is_followed
    
    @is_followed.setter
    def is_followed(self, value):
        self.__is_followed = value