# Django settings for BookShare project.

import os
from os.path import dirname

from django.conf import global_settings
from django.core.exceptions import ImproperlyConfigured
from path import path

# here is settings directory
PROJECT_ROOT = path(dirname(__file__)) / ".."

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_variable('BOOKSHARE_SECRET_KEY')

TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']
DEBUG = True

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
    'bootstrap3',
    'south',
]

BOOKSHARE_APPS = [
    'bookshare',
    'bookshare.apps.core',
    'bookshare.apps.users',
    'bookshare.apps.books',
    'bookshare.apps.console',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + BOOKSHARE_APPS

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bookshare.middleware.AssertionErrorMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages'
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

LOGIN_URL = '/signin/'
LOGOUT_URL = '/signout/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    PROJECT_ROOT / 'static',
)

TEMPLATE_DIRS = (
    PROJECT_ROOT / 'templates',
)

AUTH_USER_MODEL = 'users.User'

MEDIA_ROOT = PROJECT_ROOT / ".." / 'media'

STATIC_ROOT = PROJECT_ROOT / '..' / 'static'

MEDIA_URL = '/media/'
