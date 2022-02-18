from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, Post, RareUser


class CommentView(ViewSet):
    # match pk that comes from url
    def retrieve(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = GetCommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        comments = Comment.objects.all()
        author = RareUser.objects.get(user=request.auth.user)
        for comment in comments:
            if comment.author == author:
                comment.is_owner = True
            else:
                comment.is_owner = False

        serializer = GetCommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        post = Post.objects.get(pk=request.data['post'])
        rare_user = RareUser.objects.get(user_id=request.auth.user_id)

        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=rare_user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.content = request.data['content']
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_on', 'post', 'author', 'is_owner')
        depth = 2


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'post_id')
