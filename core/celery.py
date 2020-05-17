import os

from celery import Celery

from core.settings import CELERY_BROKER_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

celery_app = Celery('asana', broker=CELERY_BROKER_URL)
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks()
