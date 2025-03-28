from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, Celery_test_api

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'celery-test', Celery_test_api, basename='celerytest')

urlpatterns = [
    path('', include(router.urls)),
]