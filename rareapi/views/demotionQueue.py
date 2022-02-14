from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import DemotionQueue

class DemotionQueueView(ViewSet):
#match pk that comes from url
    def retrieve(self, request, pk):
        try:
            demotionQueue= DemotionQueue.objects.get(pk=pk)
            serializer= DemotionQueueSerializer(demotionQueue)
            return Response(serializer.data)
        except  DemotionQueue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        
    def list(self, request):
        demotionQueues=DemotionQueue.objects.all()
        game_type = request.query_params.get('type', None)
     
        serializer = DemotionQueueSerializer(demotionQueues, many=True)
        return Response(serializer.data)
    
class DemotionQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = DemotionQueue
        fields ='__all__'
        depth = 1