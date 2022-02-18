from django.forms import ValidationError
from rareapi.models import (Category, Post, PostReaction, RareUser, Reaction,
                            Subscription, Tag)
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ViewSet


class PostView(ViewSet):
    # Need to add a custom is_owner property to all posts
    def list(self, request):
        posts = Post.objects.all()
        user = RareUser.objects.get(user=request.auth.user)
        for post in posts:
            post.is_owner = post.user == user
            try:
                Subscription.objects.get(
                    follower_id=user.id, author_id=post.user.id)
                post.subscribed = True
            except Subscription.DoesNotExist:
                post.subscribed = False

            try:
                PostReaction.objects.get(post=post, user=user)
                post.reacted = True
            except PostReaction.DoesNotExist:
                post.reacted = False

        serializer = GetPostSerializer(posts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)

        post.is_owner = post.user == user

        try:
            Subscription.objects.get(
                follower_id=user.id, author_id=post.user.id)
            post.subscribed = True
        except Subscription.DoesNotExist:
            post.subscribed = False

        try:
            post_reaction = PostReaction.objects.get(post=post, user=user)
            post.reacted = post_reaction.reaction_id
            serializer = GetPostSerializer(post)
            return Response(serializer.data)
        except PostReaction.DoesNotExist:
            post.reacted = None
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

    @action(methods=['post', 'put'], detail=True)
    def react(self, request, pk):
        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        reaction = Reaction.objects.get(pk=request.data['reaction'])

        try:
            post_reaction = PostReaction.objects.get(post=post, user=user)
            post_reaction.reaction = reaction
            post_reaction.save()
            serializer = PostReactionSerializer(post_reaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except PostReaction.DoesNotExist:
            post_reaction = PostReaction.objects.create(
                user=user,
                post=post,
                reaction=reaction
            )
            serializer = PostReactionSerializer(post_reaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unreact(self, request, pk):
        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        post_reaction = PostReaction.objects.get(post=post, user=user)
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
                  'image_url', 'content', 'approved', 'tags', 'is_owner',
                  'reactions', 'subscribed', 'reacted')
        depth = 2


class CreatePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('category', 'title', 'image_url', 'content', 'tags')


class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('reaction', )
