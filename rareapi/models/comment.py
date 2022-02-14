from django.db import models

class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True) 
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comment_post")
    author_id  = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="comment_author")