from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rareapi.models import Tag


class TagView(ViewSet):
    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    def create(self, request):
        tag = Tag.objects.create(
            label = request.data['label']
        )
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.label = request.data['label']
        tag.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        tag = Tag.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        depth = 1