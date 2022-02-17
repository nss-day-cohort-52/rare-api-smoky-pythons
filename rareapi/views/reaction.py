from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rareapi.models import Reaction


class ReactionView(ViewSet):
    def list(self, request):
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        reaction = Reaction.objects.get(pk=pk)
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data)
    
    def create(self, request):
        reaction = Reaction.objects.create(
            label = request.data['label'],
            image_url = request.data['image_url']
        )
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        reaction = Reaction.objects.get(pk=pk)
        reaction.label = request.data['label']
        reaction.image_url = request.data['image_url']
        reaction.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        reaction = Reaction.objects.get(pk=pk)
        reaction.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ReactionSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"
        depth = 1