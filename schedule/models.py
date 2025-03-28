from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from django.utils import timezone

class TimelineEvent(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='timeline_events')
    start_date = models.DateField()
    end_date = models.DateField()
    dependency = models.ForeignKey('tasks.Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='dependent_events')

    def __str__(self):
        return f"{self.task.title} ({self.start_date} - {self.end_date})"

class Notification(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.task.title}"

@receiver(post_save, sender=Task)
def create_timeline_event(sender, instance, created, **kwargs):
    """
    Automatically create a TimelineEvent when a Task is created
    """
    if created:  # Only run when Task is first created, not on updates
        TimelineEvent.objects.create(
            task=instance,
            start_date=instance.start_date if hasattr(instance, 'start_date') else timezone.now().date(),
            end_date=instance.due_date if hasattr(instance, 'due_date') else timezone.now().date(),
            dependency=None  # Set this based on your needs
        )