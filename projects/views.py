from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Project, Milestone
from .serializers import ProjectSerializer, MilestoneSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            models.Q(owner=self.request.user) | 
            models.Q(team_members=self.request.user)
        ).distinct()

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def available_team_members(self, request):
        #get id in dictionary form
        users = User.objects.exclude(
            id=request.user.id
        ).exclude(
            projects__owner=request.user
        )
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Milestone.objects.filter(
            project__in=Project.objects.filter(
                models.Q(owner=self.request.user) | 
                models.Q(team_members=self.request.user)
            )
        )

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        project = Project.objects.get(id=project_id)
        if project.owner != self.request.user and not project.team_members.filter(id=self.request.user.id).exists():
            raise permissions.PermissionDenied("You don't have permission to add milestones to this project")
        serializer.save(project=project)