from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Subscription, RareUser



class SubscriptionView(ViewSet):
    # match pk that comes from url
    def retrieve(self, request, pk):
        try:
            subscription = Subscription.objects.get(pk=pk)
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        subscriptions = Subscription.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


    @action(methods=['get'], detail=False)
    def currentuser(self, request):
        user = RareUser.objects.get(user=request.auth.user)  
        subs = Subscription.objects.filter(author=user)
        serializer = SubscriptionSerializer(subs, many=True)
        return Response(serializer.data)

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
        depth = 1
