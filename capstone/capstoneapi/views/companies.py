from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from capstoneapi.models import Companies
from rest_framework import serializers
from django.http.response import HttpResponseServerError
from rest_framework import status as djstatus
from django.core.exceptions import ValidationError

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
        
        
    def create(self, request):
        """Handle POST operations for commentss
        Returns:
            Response -- JSON serialized comments instance
        """
        if not request.auth.user.is_staff:
            return Response({"message": "Permission denied"}, status=djstatus.HTTP_401_UNAUTHORIZED)
    
        companies = Companies()
        companies.name = request.data["name"]
        
        
        
        try:
            companies.save()
            serializer = CompanySerializer(companies, context={'request': request})
            return Response(serializer.data, status=djstatus.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=djstatus.HTTP_400_BAD_REQUEST)
       
     
    
    

  

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ('id', 'name')
    


