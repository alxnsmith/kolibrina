from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0k#pueww6$7pm=8*-(e316$vzd3c=1ijd$^i!3y-g^a!n0v4pc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition

INSTALLED_APPS = [
    'channels',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_admin_listfilter_dropdown',
    'rangefilter',

    'accountConfirmation',
    'admin_panel',
    'API',
    'teams',
    'authK',
    'channel_common',
    'chat',

    'games',
    'marathon',

    'Kolibrina',
    'main',
    'media',
    'payment',
    'questions',
    'rating',
    'regK',
    'rules',
    'stats',
    'userK',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Kolibrina.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static/']  # может вызывать ошибку статики.

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/mediacontent/'
MEDIA_ROOT = BASE_DIR / "mediacontent"

AUTH_USER_MODEL = 'userK.User'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'kotovvsan@ya.ru'
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = '647012277RosTelecom'
EMAIL_USE_SSL = True
EMAIL_ADMIN_USERS = 'kotovvsan@ya.ru'
ADMINS = [('Nillkizz', 'kotovvsan@ya.ru')]

ASGI_APPLICATION = 'Kolibrina.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

GENDER_CHOICES = (('Male', 'М'), ('Female', 'Ж'))
COUNTRY_CHOICES = (('RU', 'Россия'), ('UK', 'Украина'), ('BY', 'Беларусь'), ('KZ', 'Казахстан'))
TEAM_ROLES = (('COMMANDER', 'Командир'), ('BASIC', 'Базовый'), ('LEGIONARY', 'Легионер'))
TEAM_NUMBERS = (('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6))
QUESTION_SCORE_EQUALS = {'1': 0.1, '2': 0.3, '3': 0.5, '4': 0.7, '5': 0.9,
                         '6': 1.2, '7': 1.5, '8': 1.8, '9': 2.1, '10': 2.4,
                         '11': 2.8, '12': 3.2, '13': 3.7, '14': 4.1, '15': 4.5,
                         '16': 5.0, '17': 5.5, '18': 6.0, '19': 6.5, '20': 7.0,
                         '21': 7.7, '22': 8.4, '23': 9.1, '24': 10.0,
                         'd1.1': 2.8, 'd1.2': 3.2, 'd1.3': 3.7, 'd1.4': 4.1, 'd1.5': 4.5,
                         'd2.1': 5.0, 'd2.2': 5.5, 'd2.3': 6.0, 'd2.4': 6.5, 'd2.5': 7.0,
                         'zamena': 0
                         }
TIME_SCORE_EQUALS = {'10': 0.007, '20': 0.08, '30': 0.14, '40': 0.2, '50': 0.23}


DOMAIN = 'kolibrina.ru'

YANDEX_CHECKOUT_CONFIG = {'account_id': '734853',
                          'secret_key': 'live_sXm5J__8xhwtHjZzVWX7Hkog4DKD59yGtDqpd_qzinI'}
