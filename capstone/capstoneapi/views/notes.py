from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from capstoneapi.models import Notes
from rest_framework import serializers
from django.http.response import HttpResponseServerError
from rest_framework import status as djstatus
from django.core.exceptions import ValidationError

class NoteViewSet(ViewSet):
    def list(self, request):
        notes = Notes.objects.all()
        serializer = NoteSerializer(notes, many=True, context={'request':request})
        return Response(serializer.data)
    
            
        
    
       
     
    
    

  

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ('id', 'content', 'user', 'workflow')
    


