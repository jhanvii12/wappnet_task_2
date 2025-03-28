from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models

class Notification(models.Model):
    task = models.ForeignKey('tasks.Task', on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.task.title}"