from .base import *  # noqa

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework_swagger',
    'telemeta_mshs.apps.telemeta_api',
    'rdflib',
)

DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
