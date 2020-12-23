from django.conf import settings

# Celery Configuration Options
task_track_started = True
task_time_limit = 30 * 60
broker_url = settings.REDIS_URL
broker_transport_options = {'visibility_timeout': 3600}
result_backend = settings.REDIS_URL
accept_content = ['application/json']
task_serializer = 'json'
result_serializer = 'json'

