from rest_framework import serializers
from .models import TimelineEvent, Notification

class TimelineEventSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    dependency_title = serializers.CharField(source='dependency.title', read_only=True)
    project_name = serializers.CharField(source='task.project.name', read_only=True)

    class Meta:
        model = TimelineEvent
        fields = ['id', 'task', 'task_title', 'start_date', 'end_date', 'dependency', 'dependency_title', 'project_name']
        read_only_fields = ['task_title', 'dependency_title', 'project_name']

    def validate(self, data):
        # Ensure end_date is not before start_date
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date cannot be before start date.")
        # Ensure dependency is not the same as the task
        if data.get('dependency') == data['task']:
            raise serializers.ValidationError("A task cannot depend on itself.")
        # Ensure dependency belongs to the same project as the task
        if data.get('dependency') and data['dependency'].project != data['task'].project:
            raise serializers.ValidationError("Dependency must belong to the same project as the task.")
        # Ensure dependency task is completed
        if data.get('dependency') and data['dependency'].status != 'COMPLETED':
            raise serializers.ValidationError("Dependency task must be completed before this task can start.")
        return data

class NotificationSerializer(serializers.ModelSerializer):
    task_title = serializers.CharField(source='task.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    project_name = serializers.CharField(source='task.project.name', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'task', 'task_title', 'user', 'user_username', 'message', 'sent_at', 'project_name']
        read_only_fields = ['sent_at', 'task_title', 'user_username', 'project_name']