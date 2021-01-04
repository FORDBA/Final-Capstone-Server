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
        
    
        workflows = Workflows()
        workflows.due_date = request.data["due_date"]
        workflows.completion_date = request.data["completion_date"]
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
        
        
        try:
            workflows.save()
            serializer = WorkflowSerializer(workflows, context={'request': request})
            return Response(serializer.data, status=djstatus.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=djstatus.HTTP_400_BAD_REQUEST)
    
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
        # company_id = self.request.query_params.get('company_id', None)
        # if company_id is not None:
        #     workflows = workflows.filter(company_id=company_id)
        
        
        
        
        

        serializer = WorkflowSerializer(
            workflows, many=True, context={'request': request})
        return Response(serializer.data)

        ## in the response body, embed a list of the Ids of all the <Reactions>
        ## for which its true that a <PostReaction> exists in which the 
        ## <User> is this request_user and the <Post> is this post
        
    

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
    company = StateSerializer(many=False)

    class Meta:
        model = Workflows
        fields = ('id', 'due_date', 'completion_date', 'preparer', 'reviewer',
                  'processor', 'status', 'state', 'company')
        depth = 1
