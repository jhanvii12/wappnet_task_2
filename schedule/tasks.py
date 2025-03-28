# Celery tasks for scheduling notifications and alerts.
from celery import shared_task
from django.utils import timezone
from .models import Notification, TimelineEvent
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def check_task_deadlines():
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)

    # 24-hour alerts for TimelineEvent end_date, send to Task assignee
    approaching_events = TimelineEvent.objects.filter(end_date=tomorrow)
    for event in approaching_events:
        if event.task.assignee:  
            Notification.objects.create(
                task=event.task,
                user=event.task.assignee,  
                message=f"Task '{event.task.title}' is due tomorrow!"
            )
            send_mail(
                subject=f"Task '{event.task.title}' is due tomorrow!",
                message=f"Task '{event.task.title}' is due tomorrow!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[event.task.assignee.email],
                fail_silently=False,
            )