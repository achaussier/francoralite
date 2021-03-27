import os

# Reminder
ALLOWED_HOSTS = ['*']
PROJECT_ROOT = '/srv/app/'
TIME_ZONE = 'Europe/Paris'
LANGUAGES = [('fr', 'French'),
             ('en', 'English'),
             ('de', 'German'),
             ('es', 'Spanish'),
             ]
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = '/srv/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/srv/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SECRET_KEY = os.getenv('SECRET_KEY')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
AUTH_USER_MODEL = 'auth.User'

# Settings for django-bootstrap3
BOOTSTRAP3 = {
    'set_required': True,
    'set_placeholder': False,
    'error_css_class': 'has-error',
    'required_css_class': 'has-warning',
    'javascript_in_head': True,
}

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


INSTALLED_APPS = (
    'django.contrib.auth',
    'mozilla_django_oidc',  # Load after auth
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
#    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_extensions',
    'timezones',
    'bootstrap3',
    'bootstrap_datepicker',
    'bootstrap_pagination',
    'registration',
    'rest_framework',
    'rest_framework_xml',
    'django',
    'drf_yasg',
    'django_filters',
    'telemeta_mshs.apps.telemeta_api',
    'telemeta_mshs.apps.telemeta_front',
    'django_select2',
    'leaflet',
    'markdownx',
    'corsheaders',
    'rdflib',
    # Check if always needed
    'extra_views',
)

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'telemeta_mshs.middleware.keycloak_mw.KeycloakMiddleware',
    'telemeta_mshs.middleware.session_history.SessionHistoryMiddleware',
    # 'telemeta_mshs.middleware.history_records.HistoryRecordsMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'NAME': os.getenv('MYSQL_DATABASE'),
        'HOST': 'db',
        'PORT': '3306',
        'TEST': {
            'NAME': 'telemeta_testing',
            'USER': 'root'
        }
    }
}

APPEND_SLASH = False

FRONT_HOST_URL = 'http://localhost:8000'
FRONT_HOST_URL_EXTERNAL = 'http://nginx.francoralite.localhost:8080'
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
USE_X_FORWARDED_PROTO = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
}

ROOT_URLCONF = 'telemeta_mshs.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'telemeta_mshs.wsgi.application'


#
# KEYCLOAK
#

# Excempt list - URL paths that doesn't need Keycloak Authorization
KEYCLOAK_BEARER_AUTHENTICATION_EXEMPT_PATHS = [
    'admin',
]
KEYCLOAK_RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgP/m+V2owmzi6egBGQekKThsXuSDsEKfWjYNk9quCCR4BBFlT0444b1xb948w7Ii59OFor3UDfvy8+mD9XSm56ghuWhvuvAcOEGYPlvqOPQ+p5IXum1b7LrjH1aljtDmT6C6No1D+POzsLy9MQBRto7zTbi3ViQoh+7tMywUPm6WreYxpwPTDhSCA2+uptPJn2R5vqi/OB4wIvQ90JXvH6RE5oSkmHSMW10UWRFGNtCABJy4XXlCXDDl6BW+uTuy1LvVZxDiqBudqEmsbeVl2gXGp46BRqs+YDabh10V7rkuF4XeHY4bU3ICfWu+1Zq7fRF1Em/cMVuUfjKXy3dKZwIDAQAB
-----END PUBLIC KEY-----"""
KEYCLOAK_CONFIG = {
    'KEYCLOAK_REALM':  'francoralite',
    'KEYCLOAK_CLIENT_ID': 'francoralite',
    'KEYCLOAK_DEFAULT_ACCESS': 'ALLOW',
    'KEYCLOAK_AUTHORIZATION_CONFIG': '/tmp/authorization_config.json',
    'KEYCLOAK_METHOD_VALIDATE_TOKEN': 'DECODE',
    'KEYCLOAK_SERVER_URL': 'http://keycloak.francoralite.localhost:8080/auth/',
    'KEYCLOAK_CLIENT_SECRET_KEY': 'cc453f2d-9342-4924-bbb9-53f3eda5e824',
    'KEYCLOAK_CLIENT_PUBLIC_KEY': KEYCLOAK_RSA_PUBLIC_KEY,
}


#
# CORS
#
CORS_ORIGIN_WHITELIST = (
    'http://1.2.3.4',
    'http://nginx.francoralite.localhost',
)

AUTHENTICATION_BACKENDS = (
    'telemeta_api.oidc.myoidcab.MyOIDCAB',
)
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_CLIENT_ID = 'francoralite'
OIDC_RP_CLIENT_SECRET = 'cc453f2d-9342-4924-bbb9-53f3eda5e824'
OIDC_CREATE_USER = True

OIDC_OP_AUTHORIZATION_ENDPOINT = \
    'http://keycloak.francoralite.localhost:8080/auth/' +\
    "realms/francoralite/protocol/openid-connect/auth"
OIDC_OP_TOKEN_ENDPOINT = 'http://keycloak.francoralite.localhost:8080/auth/' +\
    "realms/francoralite/protocol/openid-connect/token"
OIDC_OP_USER_ENDPOINT = 'http://keycloak.francoralite.localhost:8080/auth/' +\
    "realms/francoralite/protocol/openid-connect/userinfo"
OIDC_OP_JWKS_ENDPOINT = 'http://keycloak.francoralite.localhost:8080/auth/' +\
    "realms/francoralite/protocol/openid-connect/certs"


LOGIN_REDIRECT_URL = "http://nginx.francoralite.localhost:8080/"
LOGOUT_REDIRECT_URL = 'http://keycloak.francoralite.localhost:8080/auth/' +\
    "realms/francoralite/protocol/openid-connect/logout"

#
# DEBUG MANAGEMENT
#
if os.getenv('DEBUG').lower() == "true":
    DEBUG = True
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
    }
    INTERNAL_IPS = ['127.0.0.1', '0.0.0.0', '172.17.0.1']
