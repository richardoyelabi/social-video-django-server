"""
Django settings for djangoserver project.

Generated by 'django-admin startproject' using Django 4.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

import os.path

from rest_framework.permissions import IsAuthenticated

from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ylzr4838#$pl0e*a9=gra2)m$ih8v6xbz-=p=*-rr3!7$wrp_z"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 3rd party apps that have to come first
    "daphne",
    # Default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # 3rd party apps
    "rest_framework",
    "corsheaders",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "drf_spectacular",
    "versatileimagefield",
    "rest_framework_word_filter",
    "django_celery_beat",
    # Local
    "domains.apps.DomainsConfig",
    "accounts.apps.AccountsConfig",
    "transactions.apps.TransactionsConfig",
    "subscriptions.apps.SubscriptionsConfig",
    "media.apps.MediaConfig",
    "sage_stream.apps.SageStreamConfig",
    "video_purchases.apps.VideoPurchasesConfig",
    "posts.apps.PostsConfig",
    "video_saves.apps.VideoSavesConfig",
    "chats.apps.ChatsConfig",
    "special_requests.apps.SpecialRequestsConfig",
    "tips.apps.TipsConfig",
    "verifications.apps.VerificationsConfig",
    "notifications.apps.NotificationsConfig",
    # 3rd party apps that have to come last
    "django_cleanup.apps.CleanupConfig",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangoserver.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "djangoserver.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "djangoserver",
        "USER": "richard",
        "PASSWORD": "postgres",
        "HOST": "database",
        "PORT": "",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "accounts.Account"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media_files/")

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.CursorPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://localhost:8000",
)

CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SITE_ID = 1
SITE_DISPLAY = "x-app"
SITE_DOMAIN = "127.0.0.1:8000"

# ALLAUTH
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
LOGIN_URL = "http://localhost:8000/account/login/"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "accounts.serializers.CustomRegisterSerializer"
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# REDIS
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0


# CHANNELS
ASGI_APPLICATION = "djangoserver.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}


# CELERY
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {
    "update_currency_exchange_task": {
        "task": "transactions.tasks.update_currency_exchange_rate",
        "schedule": timedelta(minutes=30),  # GET NEW EXCHANGE RATE EVERY THIRTY MINUTES
    },
}


VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "profile_photo": [
        ("full_size", "thumbnail__400x400"),
        ("thumbnail", "thumbnail__100x100"),
    ],
    "cover_photo": [
        ("full_size", "thumbnail__1500x500"),
        ("thumbnail", "thumbnail__600x200"),
    ],
    "photo_upload": [("main_media", "url"), ("thumbnail", "thumbnail__300x300")],
}

STREAM_DEFAULT_PERMISSION_CLASSES = (IsAuthenticated,)
