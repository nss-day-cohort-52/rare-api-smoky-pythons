from django.db import models


class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="comment_post")
    author = models.ForeignKey(
        "RareUser", on_delete=models.CASCADE, related_name="comment_author")

    @property
    def is_owner(self):
        return self.__is_owner

    @is_owner.setter
    def is_owner(self, value):
        self.__is_owner = value
