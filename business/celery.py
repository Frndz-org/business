import os

from celery import Celery


# Indicate Celery to use the default Django settings module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business.settings')

app = Celery('business')

app.config_from_object('django.conf:settings', namespace="CELERY")

# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks()
