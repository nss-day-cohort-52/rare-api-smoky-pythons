from posixpath import realpath
from django.db import models

class PostReaction(models.Model):
    user = models.ForeignKey('RareUser', on_delete=models.CASCADE, related_name='post_reaction_user')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_reaction_post')
    reaction = models.ForeignKey('Reaction', on_delete=models.CASCADE, related_name='post_reaction_reaction')