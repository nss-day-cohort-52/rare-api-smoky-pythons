from django.db import models

class Post(models.Model):
    user = models.ForeignKey('RareUser', on_delete=models.CASCADE, related_name='post_user')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='post_category')
    title = models.CharField(max_length=120)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.URLField()
    content = models.CharField(max_length=1000)
    approved = models.BooleanField()
    tags = models.ManyToManyField(
        "Tag", through="PostTag", related_name="tags")