from rest_framework import serializers
from .models import Comment, FileAttachment
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

User = get_user_model()

class FileAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)

    class Meta:
        model = FileAttachment
        fields = ['id', 'file', 'uploaded_at', 'uploaded_by']
        read_only_fields = ['uploaded_at', 'uploaded_by']

    def create(self, validated_data):
        file = validated_data.pop('file')
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        validated_data['file'] = file_name
        return super().create(validated_data)

# Support threaded comments tied to specific tasks or projects.
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Shows the username instead of ID
    task = serializers.PrimaryKeyRelatedField(read_only=True)  # Task ID only
    project = serializers.PrimaryKeyRelatedField(read_only=True)  # Project ID only

    class Meta:
        model = Comment
        fields = ['id', 'task', 'project', 'user', 'content', 'timestamp']
        read_only_fields = ['timestamp', 'project', 'user']
