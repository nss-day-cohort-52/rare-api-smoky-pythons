from django.db import models

class Subscription(models.Model):
    created_on = models.DateField()
    ended_on = models.DateField
    author_id  = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    follower_id = models.ForeignKey("RareUser", on_delete=models.CASCADE)