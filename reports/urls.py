from django.urls import path
from .views import ProjectReportView, ProjectTaskListView, ProjectMilestoneListView

urlpatterns = [
    path('project-report/<int:project_id>/', ProjectReportView.as_view(), name='project-report'),
    path('project/<int:project_id>/tasks/', ProjectTaskListView.as_view()), 
    path('project/<int:project_id>/milestone/', ProjectMilestoneListView.as_view()),
]