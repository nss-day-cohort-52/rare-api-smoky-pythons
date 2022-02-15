from unicodedata import category
from django.forms import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rareapi.models import Post, RareUser, Tag, Category


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
        user = RareUser.objects.get(pk=request.auth.user_id)
        tags = []

        for tag_id in request.data['tags']:
            tag = Tag.objects.get(pk=tag_id)
            tags.append(tag)

        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid()
        post_obj = serializer.save(user=user)
        post_obj.tags.set(tags)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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


class GetPostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date',
                  'image_url', 'content', 'approved', 'tags', 'is_owner')
        depth = 2


class CreatePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('category', 'title', 'image_url', 'content', 'tags')
