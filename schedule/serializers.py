from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    project_name = serializers.CharField(source='task.project.name', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'task', 'task_title', 'user', 'user_username', 'message', 'sent_at', 'is_read', 'project_name']
        read_only_fields = ['sent_at', 'task_title', 'user_username', 'project_name']