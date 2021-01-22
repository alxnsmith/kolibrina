from Kolibrina.settings import *
#
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }

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

del STATIC_ROOT
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

CELERY_BROKER_URL = REDIS_URL
