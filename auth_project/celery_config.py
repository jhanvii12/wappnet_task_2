# auth_project/celery_config.py
from celery import Celery
from celery.schedules import crontab
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_project.settings')

app = Celery('auth_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-task-deadlines-daily': {
        'task': 'schedule.tasks.check_task_deadlines',
        'schedule': crontab(hour=18, minute=46), # daily at 6:06 PM  
    },
}
# app.conf.timezone = 'UTC'
app.conf.enable_utc = False
app.conf.timezone = 'Asia/Kolkata'