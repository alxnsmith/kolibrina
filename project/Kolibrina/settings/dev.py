from Kolibrina.settings.base import *

REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_URL, ],
        },
    },
}

DEBUG = True

DOMAIN = 'localhost:8000'

ADMINS = [('Nillkizz', 'kotovvsan@ya.ru')]
YANDEX_CHECKOUT_CONFIG = {'account_id': '742930',
                          'secret_key': 'test_4Yc8ayWUcMtNKy8RlHjKtgP4aDrcnIy9Xyiq_GYkOVI'}

# STATIC_ROOT = STATIC_DIR
STATICFILES_DIRS = [
    'static',
]

CELERY_BROKER_URL = REDIS_URL
