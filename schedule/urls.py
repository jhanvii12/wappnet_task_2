from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimelineEventViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'timeline-events', TimelineEventViewSet, basename='timelineevent')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]