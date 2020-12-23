from Kolibrina.settings import *
#
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_URL],
        },
    },
}

DEBUG = True
REDIS_DB = 1

DOMAIN = 'dev.kolibrina.ru'
del STATIC_ROOT
STATICFILES_DIRS = [BASE_DIR / 'static/']  # может вызывать ошибку статики в daphne.

YANDEX_CHECKOUT_CONFIG = {'account_id': '742930',
                          'secret_key': 'test_4Yc8ayWUcMtNKy8RlHjKtgP4aDrcnIy9Xyiq_GYkOVI'}

REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
CELERY_BROKER_URL = REDIS_URL
