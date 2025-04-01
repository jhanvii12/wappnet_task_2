from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Comment, FileAttachment
from .serializers import FileAttachmentSerializer, CommentSerializer
from tasks.models import Task
from projects.models import Project
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

class FileAttachmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FileAttachmentSerializer(data=request.data)
        if serializer.is_valid():
            task_id = request.data.get('task')
            project_id = request.data.get('project')
            if task_id:
                try:
                    task = Task.objects.get(pk=task_id)
                    serializer.validated_data['task'] = task
                except Task.DoesNotExist:
                    return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            if project_id:
                try:
                    project = Project.objects.get(pk=project_id)
                    serializer.validated_data['project'] = project
                except Project.DoesNotExist:
                    return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
            file = request.FILES.get('file')
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                return Response({'error': 'File size exceeds 10MB'}, status=status.HTTP_400_BAD_REQUEST)
            if not file.name.endswith(('.pdf', '.jpg', '.jpeg', '.png', '.mp4', '.avi', '.mov')):
                return Response({'error': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)
            if FileAttachment.objects.filter(file=file).exists():
                return Response({'error': 'File already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            attachment = FileAttachment.objects.get(pk=pk)
            serializer = FileAttachmentSerializer(attachment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FileAttachment.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-timestamp')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication for CRUD

    def perform_create(self, serializer):
        """ Automatically assign the authenticated user when creating a comment. """
        task_id = self.request.data.get("task")
        project_id = self.request.data.get("project")

        print(f"Received task ID: {task_id}")  # Debugging
        print(f"Received project ID: {project_id}")  # Debugging

        task = Task.objects.get(pk=task_id) if task_id else None
        project = Project.objects.get(pk=project_id) if project_id else None

        print(f"Resolved Task Object: {task}")  # Debugging
        print(f"Resolved Project Object: {project}")  # Debugging

        serializer.save(user=self.request.user, task=task, project=project)

    def get_queryset(self):
        """
        Optionally filter comments by `task_id` or `project_id` if provided in query params.
        """
        queryset = Comment.objects.all()
        task_id = self.request.query_params.get('task_id')
        project_id = self.request.query_params.get('project_id')

        if task_id:
            queryset = queryset.filter(task__id=task_id)
        if project_id:
            queryset = queryset.filter(project__id=project_id)

        return queryset

    @action(detail=False, methods=['get'])
    def mycomments(self, request):
        """ Return only the comments made by the authenticated user. """
        comments = Comment.objects.filter(user=request.user)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)