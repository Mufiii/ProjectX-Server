from __future__ import absolute_import , unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import datetime, timedelta


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ProjectX.settings')

# create a Celery instance and configure it using the configuration file.
app = Celery('ProjectX')


app.conf.update(timezone = 'Asia/Kolkata')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings' , namespace='CELERY')


app.conf.beat_schedule = {
    "send_emails": {
        "task": "tasks.send_email_task",
        "schedule": timedelta(days=1),  
    }
}


# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
  print(f'Request: {self.request!r}')
  
