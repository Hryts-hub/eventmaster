import os

from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventmaster.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventmaster.Postgre_settings.settings')

app = Celery('eventmaster')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()