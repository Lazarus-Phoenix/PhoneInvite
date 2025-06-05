from datetime import timedelta
from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env файла

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = os.getenv("SECRET_KEY", 'django-insecure-default-key')
SECRET_KEY = 'django-insecure-_u2*(5w#957yl=xx-+gd$83aun3^jkfk9^2cxd7+!%bq9(kij%'

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'phonenumber_field',
    'users',
    'rest_framework',
    'drf_yasg',
    "django_celery_beat",
    "django_celery_results",
    'celery'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Добавляем папку templates в корне проекта
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

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'POSTGRES_DB': os.getenv('POSTGRES_DB'),
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST'),
        'POSTGRES_PORT': os.getenv('POSTGRES_PORT'),
    }
}


# Custom User model
AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=300),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Для разработки, в продакшене нужно ограничить
CORS_ALLOW_CREDENTIALS = True

# Phone number settings
PHONENUMBER_DEFAULT_REGION = 'RU'
PHONENUMBER_DB_FORMAT = 'NATIONAL'

# Настройки для Celery

# URL-адрес брокера сообщений
CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL", "redis://redis:6379/0"
)  # Например, Redis, который по умолчанию работает на порту 6379

# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

# Часовой пояс для работы Celery
CELERY_TIMEZONE = TIME_ZONE

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60
"""
DatabaseScheduler хранит все расписания задач в базе данных Django.
Это позволяет управлять задачами через административную панель Django и изменять расписание в реальном времени.
"""
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

"""
PersistentScheduler хранит расписание в локальном файле celerybeat-schedule.
Это простой вариант, но менее гибкий в управлении задачами.
"""
# CELERY_BEAT_SCHEDULER = "celery.beat.PersistentScheduler"

"""
Запуск задачи раз в день при работающем CELERY
"""

CELERY_BEAT_SCHEDULE = {
    "check_last_login": {
        "task": "users.tasks.check_last_login",
        "schedule": timedelta(days=1),
    },
}

# # Cache settings (для хранения кодов подтверждения)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake',
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # Используем БД 1 (не 0 как для Celery)
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,  # Таймаут подключения в секундах
            "SOCKET_TIMEOUT": 5,          # Таймаут операций
            "IGNORE_EXCEPTIONS": True,    # Продолжать работу при ошибках Redis
        }
    }
}

# SMS settings (если будете использовать)
SMS_API_KEY = os.getenv('SMS_API_KEY')
SMS_SENDER = os.getenv('SMS_SENDER', 'INVITE')

# # Session settings
# SESSION_COOKIE_AGE = 1209600  # 2 недели
# SESSION_SAVE_EVERY_REQUEST = True

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'apiKey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}