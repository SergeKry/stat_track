import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stat_track.settings")
app = Celery("stat_track")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
