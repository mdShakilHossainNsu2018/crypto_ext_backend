"""
Django settings for crypto_ext_backend project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-azn4ttqvbj)1ihs7@^f@rzdd3&x*$8#x5zsxon06wr8amc+bzu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',

    'channels',
    'chat',
    'core',
    'eth',
    'errors',
    'top_gainer_losser',

]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crypto_ext_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'crypto_ext_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
# SQL_ENGINE=django.db.backends.postgresql
# SQL_DATABASE=hello_django_dev
# SQL_USER=hello_django
# SQL_PASSWORD=hello_django
# SQL_HOST=db
# SQL_PORT=5432

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql", #os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
#         "NAME": os.environ.get('POSTGRES_NAME'),# os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
#         "USER": os.environ.get('POSTGRES_USER'),
#         "PASSWORD": os.environ.get('POSTGRES_PASSWORD'),
#         "HOST": 'db',
#         "PORT": 5432,
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django chanel setup

ASGI_APPLICATION = "crypto_ext_backend.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
            "capacity": 1500,  # default 100

        },
    },
}

# Celery Setting
CELERY_TIMEZONE = "Australia/Tasmania"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# For celery result
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

CELERY_IMPORTS = [
    'core.consumers',
    'eth.consumers',
    'core.tasks',
    'eth.tasks',
    'errors.tasks',
    'top_gainer_losser.tasks'
]

CELERY_BEAT_SCHEDULE = {
    'send_crypto_message-10-sec': {
        'task': 'core.consumers.send_crypto_message',
        'schedule': 10.0,
        # 'args': (16, 16),
        'options': {
            'expires': 5.0,
        },
    },
    'send_gas_message-10-sec': {
        'task': 'eth.consumers.send_gas_message',
        'schedule': 10.0,
        # 'args': (16, 16),
        'options': {
            'expires': 5.0,
        },
    },
    'get_and_save_gainer_losser_object': {
        'task': 'top_gainer_losser.tasks.get_and_save_gainer_losser_object',
        'schedule': timedelta(minutes=30),
    },

    'get_and_save_crypto_top_gainer_loser': {
        'task': 'top_gainer_losser.tasks.get_and_save_crypto_top_gainer_loser',
        'schedule': timedelta(minutes=2),
    },

    'cleanup_core': {
        'task': 'core.tasks.clean_up_core_object',
        # 'schedule': crontab(),
        # midnight
        'schedule': crontab(minute=0, hour=0),
        'options': {
            'expires': 5.0,
        },
    },

    'cleanup_eth': {
        'task': 'eth.tasks.clean_up_eth_object',
        # 'schedule': crontab(),
        # midnight
        'schedule': crontab(minute=0, hour=0),
        'options': {
            'expires': 5.0,
        },
    },

    'cleanup_errors': {
        'task': 'errors.tasks.clean_up_error_object',
        # 'schedule': crontab(),
        # midnight
        'schedule': crontab(minute=0, hour=0),
        'options': {
            'expires': 5.0,
        },
    },

}

# django setting.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

# Django celery setup
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'

CRYPTO_GROUP = "CRYPTO_GROUP"
CRYPTO_ROOM = "CRYPTO_ROOM"
CRYPTO_ALARM_ROOM = "CRYPTO_ALARM_ROOM"

ETH_GAS_GROUP = "ETH_GAS_GROUP"
ETH_GAS_ROOM = "ETH_GAS_ROOM"

BTC_GROUP = "BTC_GROUP"
CRYPTO_ALARM_GROUP = "CRYPTO_ALARM_GROUP"
