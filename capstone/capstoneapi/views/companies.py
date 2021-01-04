from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from capstoneapi.models import Companies
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.http.response import HttpResponseServerError

class CompanyViewSet(ViewSet):
    def list(self, request):
        companies = Companies.objects.all()
        serializer = CompanySerializer(companies, many=True, context={'request':request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # SELECT * FROM levelupapi_gametype WHERE id = ?
            company = Companies.objects.get(pk=pk)

            serializer = CompanySerializer(
                company, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
       
     
    
    

  

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ('id', 'name')
    


