from rest_framework import serializers
from .models import Project, Milestone
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ['id', 'title', 'description', 'due_date', 'project']
        read_only_fields = ['project']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    team_members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )
    team_members_detail = UserSerializer(many=True, read_only=True, source='team_members')
    milestones = MilestoneSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'owner', 'team_members', 'team_members_detail', 'milestones']

    def create(self, validated_data):
        team_members_data = validated_data.pop('team_members')
        project = Project.objects.create(owner=self.context['request'].user, **validated_data)
        project.team_members.set(team_members_data)
        return project

    def update(self, instance, validated_data):
        team_members_data = validated_data.pop('team_members', None)
        instance = super().update(instance, validated_data)
        if team_members_data is not None:
            instance.team_members.set(team_members_data)
        return instance