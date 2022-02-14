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


class ReactionSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = "__all__"
        depth = 1