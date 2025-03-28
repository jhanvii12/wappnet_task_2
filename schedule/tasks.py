# Celery tasks for scheduling notifications and alerts.
from celery import shared_task
from django.utils import timezone
from tasks.models import Task
from .models import Notification
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def check_task_deadlines():
    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)

    # 24-hour alerts to send to Task assignee
    approaching_events = Task.objects.filter(due_date=tomorrow)
    print(approaching_events)
    for event in approaching_events:
        if event.assignee:  
            Notification.objects.create(
                task=event,
                user=event.assignee,  
                message=f"Task '{event.title}' is due tomorrow!"
            )
            send_mail(
                subject=f"Task '{event.title}' is due tomorrow!",
                message=f"Task '{event.title}' is due tomorrow!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[event.assignee.email],
                fail_silently=False,
            )

import time
# print to console for testing
@shared_task
def print_to_console():
    time.sleep(5)
    print("Celery task initiated!")