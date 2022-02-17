from django.db import models

class Subscription(models.Model):
    created_on = models.DateField(auto_now_add=True)
    ended_on = models.DateField()
    author  = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="subscription_author_id")
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="subscription_follower_id")