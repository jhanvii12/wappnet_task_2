from rest_framework import serializers
from django.contrib.auth import get_user_model
from tasks.models import Task
from projects.models import Milestone, Project

User = get_user_model()

class TaskListSerializer(serializers.ModelSerializer):
    assignee_username = serializers.CharField(source='assignee.username', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 
                 'start_date', 'due_date', 'assignee_username', 'project_name',
                 'created_at', 'updated_at']
        
class MilestoneListSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Milestone
        fields = ['id', 'title', 'description', 'due_date', 'project_name']

class ProjectReportSerializer(serializers.Serializer):
    def get_projectreport(self, project_id): 
        project = Project.objects.get(id=project_id)
        project_title = project.name  
        total_tasks = Task.objects.filter(project_id=project.id).count()
        completed_tasks = Task.objects.filter(project_id=project.id, status='COMPLETED').count()  
        pending_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks else 0 
        return {
            'project': project.id,
            'project_title': project_title,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'completion_rate': completion_rate,  
        }