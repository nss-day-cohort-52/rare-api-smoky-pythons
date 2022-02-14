from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Category

class CategoryView(ViewSet):
#match pk that comes from url
    def retrieve(self, request, pk):
        try:
            category= Category.objects.get(pk=pk)
            serializer= CategorySerializer(category)
            return Response(serializer.data)
        except  Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request):
        categories=Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields ='__all__'
        depth = 1
        