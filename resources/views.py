from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import models
from django.db.models import Sum
from rest_framework.decorators import action
from .models import ResourceAllocation, Resource
from .serializers import ResourceAllocationSerializer, ResourceSummarySerializer

class ResourceAllocationViewSet(viewsets.ModelViewSet):
    queryset = ResourceAllocation.objects.all()
    serializer_class = ResourceAllocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ResourceAllocation.objects.filter(
            models.Q(task__assignee=user) | 
            models.Q(task__project__team_members=user)
        ).distinct()
    
    def perform_create(self, serializer):
        resource_allocation = serializer.save()
        return Response(serializer.data, status=201)    
    
    def perform_update(self, serializer):
        resource_allocation = serializer.save()
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        user = self.request.user
        # Get all resources for projects the user is involved in
        resources = Resource.objects.filter(
            models.Q(project__team_members=user) | 
            models.Q(project__resource_allocations__task__assignee=user)
        ).distinct()

        # Calculate allocated quantities per resource type and project
        allocations = ResourceAllocation.objects.filter(
            project__in=resources.values('project')
        ).values('project', 'resource_type').annotate(
            allocated_quantity=Sum('allocated_quantity')
        )

        # Build summary data
        summary_data = []
        for resource in resources:
            allocated = next(
                (a['allocated_quantity'] for a in allocations 
                 if a['project'] == resource.project_id and a['resource_type'] == resource.resource_type), 
                0
            )
            summary_data.append({
                'project_id': resource.project_id,
                'project': resource.project,
                'resource_type': resource.resource_type,
                'total_quantity': resource.total_quantity,
                'allocated_quantity': allocated,
                'available_quantity': resource.total_quantity - allocated
            })

        serializer = ResourceSummarySerializer(summary_data, many=True)
        return Response(serializer.data)