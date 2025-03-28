from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .tasks import check_task_deadlines, print_to_console

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter notifications for the authenticated user
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        # Fetch unread notifications
        unread_notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Send notification asynchronously
        # check_task_deadlines.delay(serializer.data)

class Celery_test_api(viewsets.ViewSet):
    def list(self, request):
        print_to_console.delay()
        return Response({"message": "Celery task initiated!"})