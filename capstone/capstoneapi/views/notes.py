from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from capstoneapi.models import Notes, Workflows, WorkflowUsers
from rest_framework import serializers
from django.http.response import HttpResponseServerError
from rest_framework import status as djstatus
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class NoteViewSet(ViewSet):

    def create(self, request):
        """Handle POST operations for commentss
        Returns:
            Response -- JSON serialized comments instance
        """
        author = WorkflowUsers.objects.get(user=request.auth.user)
        
        notes = Notes()
        notes.content = request.data["content"]
        notes.author = author
        workflows = Workflows.objects.get(pk=request.data["workflow"])
        notes.workflow = workflows
        
        try:
            notes.save()
            serializer = NoteSerializer(notes, context={'request': request})
            return Response(serializer.data, status=djstatus.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=djstatus.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """Handle GET requests to comments resource
        Returns:
            Response -- JSON serialized list of comments
        """
        notes = Notes.objects.all()
        workflow_id = request.query_params.get('workflow_id', None)
        if workflow_id is not None:
            notes = notes.filter(workflow_id=workflow_id)
        serializer = NoteSerializer(
            notes, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        """ Handle PUT request to comments; only content and subject fields are 
            editable as currently specified in project requirements
         """
        try: 
            note = Notes.objects.get(pk=pk)
        except Notes.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=djstatus.HTTP_404_NOT_FOUND)

        workflow_user = WorkflowUsers.objects.get(user=request.auth.user)
        if note.author != workflow_user:
            return Response(
                {'message': 'Notes cannot be updated by users who did not author them.'},
                status=djstatus.HTTP_403_FORBIDDEN
            )

        note.content = request.data["content"]
       
        try:
            note.save()
            return Response({}, status=djstatus.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=djstatus.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            note = Notes.objects.get(pk=pk)
        except Notes.DoesNotExist as ex:
            return Response({'message': ex.args[0]})

        workflow_user = WorkflowUsers.objects.get(user=request.auth.user)
        if note.author != workflow_user:
            return Response(
                {'message': 'Comments can only be deleted by the users who authored them.'},
                status=djstatus.HTTP_403_FORBIDDEN
            )
        
        try:
            note.delete()
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=djstatus.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({}, status=djstatus.HTTP_204_NO_CONTENT)




class WorkflowUsersSerializer(serializers.ModelSerializer):
    """JSON serializer for Users"""

    class Meta:
        model = WorkflowUsers
        fields = ['id', 'fullname']

class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for note creator"""
    author = WorkflowUsersSerializer()
    
    class Meta:
        model = Notes
        fields = ('id','author', 'content')









