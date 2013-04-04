import os
import sys
import dj_database_url
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///%s' % os.path.join(os.path.dirname(__file__), '..', '..', '..', 'db.sqlite3')),
}

ALLOWED_HOSTS = [
    'vapemap.herokuapp.com',
    'www.vapemap.co.uk',
    'www.vapourhunter.co.uk',
    'www.vapourhunter.com',
]

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(__file__), 'static'),
    ]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = [
    os.path.join(os.path.dirname(__file__), '..', 'templates'),
]


SECRET_KEY = '4-jz1w*@m**o4dk6!%e22xq3aj!r^9+y(s+_8)v-+)v4fz1lsa'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'gunicorn',
    'raven.contrib.django.raven_compat',
    'south',
    'waffle',
    'storages',
    'markdown_deux',
    'epiceditor',
    'bootstrapform',
    'registration',
    'haystack',
    'stores',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'waffle.middleware.WaffleMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'stores.context_processors.site',
    'stores.context_processors.pending_admin',
)

ROOT_URLCONF = 'vapemap.urls'
WSGI_APPLICATION = 'vapemap.wsgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', 'console'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ.get('FOUNDELASTICSEARCH_URL', 'http://127.0.0.1:9200/'),
        'INDEX_NAME': 'vapemap-haystack',
    },
}