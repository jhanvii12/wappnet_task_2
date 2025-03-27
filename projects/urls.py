#without using router
from django.urls import path
from .views import ProjectViewSet, MilestoneViewSet

urlpatterns = [
    path('project/', ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-list'),
    path('project/<int:pk>/', ProjectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='project-detail'),
    path('project/available_team_members/', ProjectViewSet.as_view({'get': 'available_team_members'}), name='available-team-members'),
    path('milestones/', MilestoneViewSet.as_view({'get': 'list', 'post': 'create'}), name='milestone-list'),
    path('milestones/<int:pk>/', MilestoneViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='milestone-detail'),
]