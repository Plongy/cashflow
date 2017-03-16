"""
Django settings for cashflow project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.conf.global_settings import AUTHENTICATION_BACKENDS, SESSION_COOKIE_AGE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# noinspection PyRedeclaration
AUTHENTICATION_BACKENDS = ['cashflow.dauth.DAuth']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '-01^^veefr*f_p=phew0w7ib37_738%=lwmp9n4bl_2*5^)vjy')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG', False))

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'expenses',
    'rest_framework',
    'storages'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'cashflow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['build'],
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

WSGI_APPLICATION = 'cashflow.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'cashflow'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASS', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# noinspection PyRedeclaration
SESSION_COOKIE_AGE = 60 * 60 * 24 * 2  # Sessions expire after 2 days

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_API_KEY = os.getenv('LOGIN2_KEY', 'key-012345678910111213141516171819')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_DIRS = ['build/static/']
STATIC_ROOT = 'build/'
STATIC_URL = '/static/'

AWS_STORAGE_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'se.datasektionen.foo')
AWS_ACCESS_KEY_ID = os.getenv('S3_ACCESS_KEY_ID', 'xxxxxxxxxxxxxxxxxxxx')
AWS_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY', 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')

AWS_S3_HOST = os.getenv('S3_HOST', 's3.eu-central-1.amazonaws.com')
AWS_S3_CUSTOM_DOMAIN = "{0}.s3.amazonaws.com".format(AWS_STORAGE_BUCKET_NAME)

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://{0}/{1}/".format(AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'expenses.custom_storages.MediaStorage'
