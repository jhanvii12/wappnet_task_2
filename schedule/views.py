from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import TimelineEvent, Notification
from .serializers import TimelineEventSerializer, NotificationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .tasks import check_task_deadlines
from tasks.models import Task

class TimelineEventViewSet(viewsets.ModelViewSet):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    # create timelineevent when task is created
    def perform_create(self, serializer):
        task = Task.objects.get(id=self.request.data['task'])
        serializer.save(task=task)
        print(serializer.data)

    def get_queryset(self):
        # Filter timeline events where the user is either the project owner, a team member, or the task assignee
        user = self.request.user
        return TimelineEvent.objects.filter(
            Q(task__project__owner=user) |
            Q(task__project__team_members=user) |
            Q(task__assignee=user)
        ).distinct()

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        # Fetch upcoming timeline events for the user
        upcoming_events = self.get_queryset().filter(start_date__gte=timezone.now().date())
        serializer = self.get_serializer(upcoming_events, many=True)
        print(serializer.data)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter notifications for the authenticated user
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        # Fetch unread notifications (assuming an 'is_read' field might be added later)
        unread_notifications = self.get_queryset().filter(sent_at__lte=timezone.now())
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Automatically set the user to the authenticated user when creating a notification
        serializer.save(user=self.request.user)
        # Send notification asynchronously
        check_task_deadlines.delay(serializer.data)