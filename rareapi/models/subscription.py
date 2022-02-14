from django.db import models

class Subscription(models.Model):
    created_on = models.DateField(auto_now_add=True)
    ended_on = models.DateField(auto_now_add=True)
    author_id  = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    follower_id = models.ForeignKey("RareUser", on_delete=models.CASCADE)