from unicodedata import category
from django.forms import ValidationError
from rareapi.models.post_reaction import PostReaction
from rareapi.models.reaction import Reaction
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.serializers import ModelSerializer
from rareapi.models import Post, RareUser, Tag, Category
from rest_framework.decorators import action



class PostView(ViewSet):
    # Need to add a custom is_owner property to all posts
    def list(self, request):
        posts = Post.objects.all()
        for post in posts:
            post.is_owner = post.user_id == request.auth.user_id

        serializer = GetPostSerializer(posts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.is_owner = post.user == request.auth.user
        serializer = GetPostSerializer(post)
        return Response(serializer.data)

    def create(self, request):
        user = RareUser.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=request.data['category'])
        tags = []

        for tag_id in request.data['tags']:
            tag = Tag.objects.get(pk=tag_id)
            tags.append(tag)

        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_obj = serializer.save(user=user, category=category)
        post_obj.tags.set(tags)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['post'], detail=True)
    def react(self, request, pk):
        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        reaction = Reaction.objects.get(pk=request.data['reactionId'])
        post_reaction = PostReaction.objects.create(
            user=user,
            post=post,
            reaction=reaction
        )
        serializer = PostReactionSerializer(post_reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def unreact(self, request, pk):
        post_reaction = PostReaction.objects.get(pk=pk)
        post_reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    

    def update(self, request, pk):
        tags = []
        post = Post.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data['category']['id'])

        post.category = category
        post.title = request.data['title']
        post.image_url = request.data['image_url']
        post.content = request.data['content']

        for tag_id in request.data['tags']:
            tag = Tag.objects.get(pk=tag_id)
            tags.append(tag)

        post.tags.set(tags)

        post.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GetPostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date',
                  'image_url', 'content', 'approved', 'tags', 'is_owner', 'reactions')
        depth = 2


class CreatePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('category', 'title', 'image_url', 'content', 'tags')
        
class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = '__all__'
        depth = 1

