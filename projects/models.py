from django.db import models

# Create your models here.
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    team_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')

    def __str__(self):
        return self.name

class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.project.name})"