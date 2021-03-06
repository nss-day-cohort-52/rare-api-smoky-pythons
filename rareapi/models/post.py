from django.db import models
from rareapi.models.reaction import Reaction

from rareapi.models.post_reaction import PostReaction


class Post(models.Model):
    user = models.ForeignKey(
        'RareUser', on_delete=models.CASCADE, related_name='post_user')
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='post_category')
    title = models.CharField(max_length=120)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.URLField(max_length=1000, blank=True)
    content = models.CharField(max_length=5000)
    approved = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        "Tag", through="PostTag", related_name="tags")

    # property decorator used to determine if the current user owns the post
    @property
    def is_owner(self):
        return self.__is_owner

    @is_owner.setter
    def is_owner(self, value):
        self.__is_owner = value

    # property decorator used to determine if the current user is subbed to the author of a post
    @property
    def subscribed(self):
        return self.__subscribed

    @subscribed.setter
    def subscribed(self, value):
        self.__subscribed = value

    # property decorator used to determine if the current user has reacted to a post
    @property
    def reacted(self):
        return self.__reacted

    @reacted.setter
    def reacted(self, value):
        self.__reacted = value
        
    @property   
    def reactions(self):
        array = []
        post_reactions = PostReaction.objects.filter(post=self)
        reactions = Reaction.objects.all()
        for reaction in reactions:
            array.append({
                "label": reaction.label,
                "count": len(post_reactions.filter(reaction=reaction))
            })
        return array
        
