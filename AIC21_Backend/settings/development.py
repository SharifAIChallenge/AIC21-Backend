"""
Django settings for AIC21_Backend project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta

from celery.schedules import crontab
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from decouple import config
from .martor import *

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!$h&e8lhno#!!4+$wt70zw&jw^v5$6%8#ev-c--!g-#6wbxm3b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',
    'martor',
    'corsheaders',
    'apps.blog',
    'apps.homepage',
    'apps.notification',
    'apps.go',
    'apps.uploads',
    'apps.faq',
    'apps.staff',
    'apps.ticket',
    'apps.accounts',
    'apps.core',
    'apps.past',
    'apps.resources',
    'apps.gamedoc',
    'apps.team',
    'apps.course',
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "dj_rest_auth.registration",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
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
    'AIC21_Backend.middlewares.Always200Middleware',
    'AIC21_Backend.middlewares.WrapSerializerErrorsMiddleware',
]

ROOT_URLCONF = 'AIC21_Backend.urls'

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

WSGI_APPLICATION = 'AIC21_Backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                + '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                + '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                + '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                + '.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_AUTHENTICATION_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        "dj_rest_auth.utils.JWTCookieAuthentication",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 100,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_REQUIRED = False

REST_USE_JWT = True

SITE_ID = 1
CORS_ORIGIN_ALLOW_ALL = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

LOGIN_REDIRECT_URL = '/api/admin/'
LOGOUT_REDIRECT_URL = '/api/admin/'

TEAM_SUBMISSION_TIME_DELTA = 1

INFRA_IP = config("INFRA_IP")
INFRA_AUTH_TOKEN = config("INFRA_AUTH_TOKEN")
INFRA_API_SCHEMA_ADDRESS = config("INFRA_API_SCHEMA_ADDRESS")

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = config('EMAIL_USE_SSL')
EMAIL_BACKEND = config('EMAIL_BACKEND')


# DOMAIN = config('DOMAIN', 'localhost:8000')

AUTH_USER_MODEL = 'accounts.User'

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'https://stg.aichallenge.ir',
    'http://stg.aichallenge.ir',
    'https://aichallenge.ir',
    'http://aichallenge.ir',
    'https://api-stg.aichallenge.ir',
    'http://api-stg.aichallenge.ir',
    'https://api.aichallenge.ir',
    'http://api.aichallenge.ir',
)
