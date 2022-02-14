from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment

class CommentView(ViewSet):
#match pk that comes from url
    def retrieve(self, request, pk):
        try:
            comment= Comment.objects.get(pk=pk)
            serializer= CommentSerializer(comment)
            return Response(serializer.data)
        except  Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request):
        comments=Comment.objects.all()
    
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields ='__all__'
        depth = 1