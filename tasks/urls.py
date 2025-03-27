from django.urls import path, include
from .views import TaskViewSet, TaskStatusViewSet

urlpatterns = [
    path('task/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),
    path('task/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='task-detail'),
    path('statuses/', TaskStatusViewSet.as_view({'get': 'list', 'post': 'create'}), name='status-list'),
    path('statuses/<int:pk>/', TaskStatusViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='status-detail'),
]