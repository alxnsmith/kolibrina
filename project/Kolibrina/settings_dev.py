from Kolibrina.settings import *

DEBUG = True
REDIS_DB = 1
DOMAIN = 'dev.kolibrina.ru'
del STATIC_ROOT
STATICFILES_DIRS = [BASE_DIR / 'static/']
