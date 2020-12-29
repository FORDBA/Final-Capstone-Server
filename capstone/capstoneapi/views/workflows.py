from django.http.response import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from capstoneapi.models import Workflows, States, Statuses, Companies, Notes
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Q


class WorkflowViewSet(ViewSet):
    
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
        
        if Q(preparer_id) & Q(processor_id) & Q(reviewer_id) is not None:
            workflows = workflows.filter(Q(preparer_id=preparer_id) | Q(processor_id=processor_id) | Q(reviewer_id=reviewer_id))

        # e.g.: /posts?company_id=1
        company_id = self.request.query_params.get('company_id', None)
        if company_id is not None:
            posts = workflows.filter(company_id=company_id)

        

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
    """Basic Serializer for single post"""
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
