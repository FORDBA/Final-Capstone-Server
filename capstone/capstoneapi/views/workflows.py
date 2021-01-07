from django.db.models.deletion import SET_NULL
from django.http.response import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status as djstatus
from capstoneapi.models import Workflows, States, Statuses, Companies, Notes
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Q


class WorkflowViewSet(ViewSet):
    
    
    def create(self, request):
        """Handle POST operations for commentss
        Returns:
            Response -- JSON serialized comments instance
        """
        if not request.auth.user.is_staff:
            return Response({"message": "Permission denied"}, status=djstatus.HTTP_401_UNAUTHORIZED)
    
        workflows = Workflows()
        workflows.due_date = request.data["due_date"]
        preparer = User.objects.get(pk=request.data["preparer"])
        workflows.preparer = preparer
        reviewer = User.objects.get(pk=request.data["reviewer"])
        workflows.reviewer = reviewer
        processor = User.objects.get(pk=request.data["processor"])
        workflows.processor = processor
        status = Statuses.objects.get(pk=request.data["status"])
        workflows.status = status
        state = States.objects.get(pk=request.data["state"])
        workflows.state = state
        company = Companies.objects.get(pk=request.data["company"])
        workflows.company = company
        if status.id == 7:
            workflows.completion_date = date.today()
        else:
            workflows.completion_date = None
        
        try:
            workflows.save()
            serializer = WorkflowSerializer(workflows, context={'request': request})
            return Response(serializer.data, status=djstatus.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=djstatus.HTTP_400_BAD_REQUEST)
        
        
    def update(self, request, pk=None):
        """ Handle PUT request to comments; only content and subject fields are 
            editable as currently specified in project requirements
         """
        try: 
            workflow = Workflows.objects.get(pk=pk)
        except Workflows.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=djstatus.HTTP_404_NOT_FOUND)
        
       
        if not request.auth.user.is_staff:
            return Response({"message": "Permission denied"}, status=djstatus.HTTP_401_UNAUTHORIZED)

       
        
        workflow.due_date = request.data["due_date"]
        preparer = User.objects.get(pk=request.data["preparer"])
        workflow.preparer = preparer
        reviewer = User.objects.get(pk=request.data["reviewer"])
        workflow.reviewer = reviewer
        processor = User.objects.get(pk=request.data["processor"])
        workflow.processor = processor
        status = Statuses.objects.get(pk=request.data["status"])
        workflow.status = status
        state = States.objects.get(pk=request.data["state"])
        workflow.state = state
        company = Companies.objects.get(pk=request.data["company"])
        workflow.company = company
        if status.id == 7:
            workflow.completion_date = date.today()
        else:
            workflow.completion_date = None
        
        
        
        
        try:
            workflow.save()
            return Response({}, status=djstatus.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=djstatus.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        """Handle GET requests to posts resource

        Returns:
            Response -- JSON serialized list of posts
        """
        
        workflows = Workflows.objects.all()
        
        
        
               

        # e.g.: /workflows?user_id=1
        preparer_id = self.request.query_params.get('preparer_id', None)
        processor_id = self.request.query_params.get('processor_id', None)
        reviewer_id = self.request.query_params.get('reviewer_id', None)
        
        if preparer_id is not None:
            workflows = workflows.filter(Q(preparer_id=preparer_id) | Q(processor_id=processor_id) | Q(reviewer_id=reviewer_id))
       

        # e.g.: /workflows?company_id=1
        company_id = self.request.query_params.get('company_id', None)
        if company_id is not None:
            workflows = workflows.filter(company_id=company_id)
        
        
        
        
        

        serializer = WorkflowSerializer(
            workflows, many=True, context={'request': request})
        return Response(serializer.data)

    
    def partial_update(self, request, pk=None):
        """Handle a partial update to a Post resource. Handles PATCH requests

        Currently this will only update the `approved` property"""

        try:
            workflow = Workflows.objects.get(pk=pk)
        except Workflows.DoesNotExist:
            return Response(
                {'message': 'There is no Workflow with the given id.'},
                status=djstatus.HTTP_404_NOT_FOUND)
        
        #Prevent non-admin users from modifying other user's posts
        

                
        
        status = Statuses.objects.get(pk=request.data["status"])
        workflow.status = status
        
        if request.data['status'] == '7':
            workflow.completion_date = date.today()
        else:
            workflow.completion_date = None

        # Save whatever has been updated in the PATCH request
        try:
            workflow.save()
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=djstatus.HTTP_400_BAD_REQUEST)

        return Response({}, status=djstatus.HTTP_204_NO_CONTENT)   
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # SELECT * FROM levelupapi_gametype WHERE id = ?
            workflow = Workflows.objects.get(pk=pk)

            serializer = WorkflowSerializer(
                workflow, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    def destroy(self, request, pk=None):
        
        try:
            workflow = Workflows.objects.get(pk=pk)

            #Prevent non-admin users from deleting posts from other users
            
            if request.auth.user.is_staff:
                workflow.delete()
                return Response({}, status=djstatus.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "Permission denied"}, status=djstatus.HTTP_401_UNAUTHORIZED)
                
        except Workflows.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=djstatus.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=djstatus.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

class PreparerSerializer(serializers.ModelSerializer):
    """Serializer for User Info in a workflow"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class ReviewerSerializer(serializers.ModelSerializer):
    """Serializer for User Info in a workflow"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class ProcessorSerializer(serializers.ModelSerializer):
    """Serializer for User Info in a workflow"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')
       
class StateSerializer(serializers.ModelSerializer):
    """Serializer for State Info in a workflow"""
    class Meta:
        model = States
        fields = ('id', 'name')
        
class CompanySerializer(serializers.ModelSerializer):
    """Serializer for State Info in a workflow"""
    class Meta:
        model = Companies
        fields = ('id', 'name')

class StatusSerializer(serializers.ModelSerializer):
    """Serializer for State Info in a workflow"""
    class Meta:
        model = Statuses
        fields = ('id', 'name')

        
class WorkflowSerializer(serializers.ModelSerializer):
    
    preparer = PreparerSerializer(many=False)
    reviewer = ReviewerSerializer(many=False)
    processor = ProcessorSerializer(many=False)    
    state = StateSerializer(many=False)
    status = StatusSerializer(many=False)
    company = CompanySerializer(many=False)

    class Meta:
        model = Workflows
        fields = ('id', 'due_date', 'completion_date', 'preparer', 'reviewer',
                  'processor', 'status', 'state', 'company')
        depth = 1
