from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.http.response import HttpResponseServerError

class UserViewSet(ViewSet):
    def list(self, request):
        users = User.objects.all()
        serializer = BasicProfileSerializer(users, many=True, context={'request':request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # SELECT * FROM levelupapi_gametype WHERE id = ?
            user = User.objects.get(pk=pk)

            serializer = BasicProfileSerializer(
                user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
       
     
    
    @action(methods=['patch'], detail=True)
    def update_active(self, request, pk=None):
        """Handle a partial update to a RareUser resource. Handles PATCH requests

        Currently this will only update the `active` property"""
        
        try:
            workflow_user = User.objects.get(pk=pk)
            
        except User.DoesNotExist:
            return Response({'message': 'user does not exit'}, status=status.HTTP_404_NOT_FOUND)
        if not request.auth.user.is_staff:
            return Response({'message':'only admins can change user active status'}, status=status.HTTP_403_FORBIDDEN)
        if request.data["is_active"] == "false":
            workflow_user.is_active = False
        else: 
            if request.data["is_active"] == "true":
                workflow_user.is_active = True
        try:
            workflow_user.save()
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    """action to toggle between admin and author status depending on message from client"""
    @action(methods=['patch'], detail=True)
    def update_role(self, request, pk=None):
        try:
            workflow_user = User.objects.get(pk=pk)
            
        except User.DoesNotExist:
            return Response({'message': 'user does not exit'}, status=status.HTTP_404_NOT_FOUND)
        if not request.auth.user.is_staff:
            return Response({'message':'only admins can change user roles'}, status=status.HTTP_403_FORBIDDEN)
        if request.data["is_staff"] == "false":
            workflow_user.is_staff = False
        else: 
            if request.data["is_staff"] == "true":
                workflow_user.is_staff = True
        try:
            workflow_user.save()
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_204_NO_CONTENT) 

class BasicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'is_active', 'first_name', 'last_name', 'email' )
    


