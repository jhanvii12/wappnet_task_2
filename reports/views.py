from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectReportSerializer, TaskListSerializer, MilestoneListSerializer
from projects.models import Project, Milestone
from tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            if request.user != project.owner and request.user not in project.team_members.all():
                return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            serializer = ProjectReportSerializer()
            report_data = serializer.get_projectreport(project_id)
            return Response(report_data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

class ProjectTaskListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            if request.user != project.owner and request.user not in project.team_members.all():
                return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
                
            tasks = Task.objects.filter(project_id=project_id)
            serializer = TaskListSerializer(tasks, many=True)
            return Response({
                "project_id": project_id,
                "project_name": project.name,
                "tasks": serializer.data
            }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProjectMilestoneListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            milestone = Milestone.objects.filter(project_id=project_id)
            serializer = MilestoneListSerializer(milestone, many=True)
            return Response({
                "project_id": project_id,
                "project_name": project.name,
                "milestone": serializer.data
            }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)