#models.py
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import DateRangeField  # Requires psycopg2

class Resource(models.Model):
    RESOURCE_TYPES = (
        ('PERSONNEL', 'Personnel'),
        ('BUDGET', 'Budget'),
        ('EQUIPMENT', 'Equipment'),
    )
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='resources')
    total_quantity = models.IntegerField()  # Total available resources for the project

    def __str__(self):
        return f"{self.resource_type} for {self.project.name}"

class ResourceAllocation(models.Model):
    RESOURCE_TYPES = (
        ('PERSONNEL', 'Personnel'),
        ('BUDGET', 'Budget'),
        ('EQUIPMENT', 'Equipment'),
    )
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='resource_allocations')
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='resource_allocations')
    allocated_quantity = models.IntegerField()
    allocation_period = DateRangeField()
    
    def __str__(self):
        return f"{self.resource_type} for {self.task.title}"