# Django settings for BookShare project.

import os
import re
from os.path import join, abspath, dirname

from django.core.exceptions import ImproperlyConfigured
from path import path

BASE_DIR = path(os.path.dirname(__file__)) / ".."
PROJECT_ROOT = BASE_DIR / ".."

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_variable('BOOKSHARE_SECRET_KEY')

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


ADMINS = (
    ('TaeYun Lee', 'ok7217@gmail.com'),
)

MANAGERS = ADMINS

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'tastypie',
]

BOOKSHARE_APPS = [
    'users',
    'books',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + BOOKSHARE_APPS

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bookshare.urls'

WSGI_APPLICATION = 'bookshare.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_ROOT / 'bookshare.sqlite',
    }
}

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    PROJECT_ROOT / 'static',
)
TEMPLATE_DIRS = (
    PROJECT_ROOT / 'templates',
)
