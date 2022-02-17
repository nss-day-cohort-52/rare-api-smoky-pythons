from crypt import methods
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from rareapi.models import RareUser


class RareUserView(ViewSet):
    def list(self, request):
        rare_users = RareUser.objects.all()
        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        rare_user = RareUser.objects.get(pk=pk)
        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def current(self, request):
        """Gets the current user at http://localhost:8000/rareusers/current"""
        rare_user = RareUser.objects.get(user=request.auth.user)
        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data)
        


class RareUserSerializer(ModelSerializer):
    class Meta:
        model = RareUser
        fields = "__all__"
        depth = 1
