from django.db import models

# Create your models here.
from django.conf import settings

class Task(models.Model):
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )
    STATUS_CHOICES = (
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='MEDIUM')
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='NOT_STARTED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskStatus(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=11, choices=Task.STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.status}"