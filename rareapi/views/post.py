from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rareapi.models import Post


class PostView(ViewSet):
    # Need to add a custom is_owner property to all posts
    def list(self, request):
        posts = Post.objects.all()
        for post in posts:
            post.is_owner = post.user_id == request.auth.user_id
            
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.is_owner = post.user == request.auth.user
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 
                  'image_url', 'content', 'approved', 'tags', 'is_owner')
        depth = 2