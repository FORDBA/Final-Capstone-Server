from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from capstoneapi.models import States
from rest_framework import serializers
from django.http.response import HttpResponseServerError

class StateViewSet(ViewSet):
    def list(self, request):
        states = States.objects.all()
        serializer = StateSerializer(states, many=True, context={'request':request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # SELECT * FROM levelupapi_gametype WHERE id = ?
            state = States.objects.get(pk=pk)

            serializer = StateSerializer(
                state, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
       
     
    
    

  

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ('id', 'name')