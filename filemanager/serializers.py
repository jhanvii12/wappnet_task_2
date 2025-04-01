from rest_framework import serializers
from .models import Comment, FileAttachment
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from tasks.models import Task
from projects.models import Project

User = get_user_model()

class FileAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False, allow_null=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False, allow_null=True)

    class Meta:
        model = FileAttachment
        fields = ['id', 'file', 'uploaded_at', 'uploaded_by', 'task', 'project']
        read_only_fields = ['uploaded_at', 'uploaded_by']

    def create(self, validated_data):
        file = validated_data.pop('file')
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        validated_data['file'] = file_name
        print(f"Validated Data Before Saving: {validated_data}")  # Debugging
        return super().create(validated_data)

# Support threaded comments tied to specific tasks or projects.
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False, allow_null=True) 
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), required=False, allow_null=True)  

    class Meta:
        model = Comment
        fields = ['id', 'task', 'project', 'user', 'content', 'timestamp']
        read_only_fields = ['timestamp', 'user']
