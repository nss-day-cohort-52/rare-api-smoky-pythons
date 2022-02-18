from crypt import methods
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from rareapi.models import RareUser, Subscription


class RareUserView(ViewSet):
    def list(self, request):
        rare_users = RareUser.objects.all()
        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        author = RareUser.objects.get(pk=pk)
        follower = RareUser.objects.get(user=request.auth.user)
        try:
            Subscription.objects.get(follower=follower, author=author)
            author.is_followed = True
            serializer = RareUserSerializer(author)
            return Response(serializer.data)   
        except Subscription.DoesNotExist:
            author.is_followed = False
            serializer = RareUserSerializer(author)
            return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def currentuser(self, request):
        """Gets the current user at http://localhost:8000/rareusers/currentuser"""
        rare_user = RareUser.objects.get(user=request.auth.user)
        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def subscribe(self, request, pk):
        author = RareUser.objects.get(pk=pk)
        follower = RareUser.objects.get(user=request.auth.user)
        serializer = SubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author, follower=follower)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unsubscribe(self, request, pk):
        author = RareUser.objects.get(pk=pk)
        follower = RareUser.objects.get(user=request.auth.user)
        sub_obj = Subscription.objects.get(
            author=author, follower=follower)
        sub_obj.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class RareUserSerializer(ModelSerializer):
    class Meta:
        model = RareUser
        fields = ('id', "bio", 'is_followed', 'created_on', 'user', 'is_followed')
        depth = 1


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('author', 'follower')
        depth = 1
