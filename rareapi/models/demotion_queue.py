from django.db import models

class DemotionQueue(models.Model):
    action = models.CharField(max_length=100)
    admin_id = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    approver_one_id = models.ForeignKey("RareUser", on_delete=models.CASCADE)