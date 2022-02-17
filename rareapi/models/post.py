from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        'RareUser', on_delete=models.CASCADE, related_name='post_user')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='post_category')
    title = models.CharField(max_length=120)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.URLField(blank=True, max_length=500)
    content = models.CharField(max_length=10000)
    approved = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        "Tag", through="PostTag", related_name="tags")

    @property
    def is_owner(self):
        return self.__is_owner

    @is_owner.setter
    def is_owner(self, value):
        self.__is_owner = value
