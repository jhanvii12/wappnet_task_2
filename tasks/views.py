from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, TaskStatus
from .serializers import TaskSerializer, TaskStatusSerializer
from django.db import models

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return tasks where the user is either the assignee or a team member of the project
        user = self.request.user
        return Task.objects.filter(
            models.Q(assignee=user) | 
            models.Q(project__team_members=user)
        ).distinct()

    def perform_create(self, serializer):
        # Automatically set the status update when creating a task
        task = serializer.save()
        TaskStatus.objects.create(task=task, status=task.status)

    def perform_update(self, serializer):
        # Create a status update when status changes
        instance = serializer.instance
        new_status = self.request.data.get('status')
        task = serializer.save()
        
        if new_status and new_status != instance.status:
            TaskStatus.objects.create(task=task, status=new_status)

class TaskStatusViewSet(viewsets.ModelViewSet):
    serializer_class = TaskStatusSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Filter status updates based on user's access to tasks
        user = self.request.user
        return TaskStatus.objects.filter(
            task__in=Task.objects.filter(
                models.Q(assignee=user) | 
                models.Q(project__team_members=user)
            )
        )

    def perform_create(self, serializer):
        # Ensure the task exists and user has permission
        task_id = self.request.data.get('task')
        task = Task.objects.filter(
            models.Q(id=task_id) & 
            (models.Q(assignee=self.request.user) | 
             models.Q(project__team_members=self.request.user))
        ).first()
        
        if not task:
            return Response(
                {"detail": "Task not found or you don't have permission"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer.save(task=task)