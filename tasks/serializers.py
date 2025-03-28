from rest_framework import serializers
from .models import Task, TaskStatus
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = ['id', 'status', 'updated_at']
        read_only_fields = ['updated_at']

class TaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        write_only=True,
        required=False,
        allow_null=True
    )
    status_updates = TaskStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assignee', 'assignee_id', 
                 'priority', 'start_date', 'due_date', 'status', 'created_at', 'updated_at', 'dependency', 'status_updates']
        read_only_fields = ['created_at', 'updated_at']