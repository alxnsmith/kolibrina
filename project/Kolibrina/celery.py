import os

from Kolibrina import celery_settings
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.

# settings_name = os.environ.get('DJANGO_SETTINGS_MODULE').split(".")[-1]

app = Celery('Kolibrina')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(celery_settings)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_online_every_10_seconds': {
        'task': 'channel_common.tasks.send_online',
        'schedule': 10,
        'args': ('online', ),
    },
}
