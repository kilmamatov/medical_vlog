import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
app = Celery()

app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule = {
    "send_email_to_user_for_verify_acc": {
        "task": "core.utils.news_api",
        "schedule": timedelta(seconds=60),
    },
}
