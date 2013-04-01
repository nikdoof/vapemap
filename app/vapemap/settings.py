import os
import sys
import dj_database_url
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

DEBUG = bool(os.environ.get('DJANGO_DEBUG', ''))
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///%s' % os.path.join(os.path.dirname(__file__), '..', '..', 'db.sqlite3')),
}

ALLOWED_HOSTS = [
    '127.0.0.1',
]

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), '..', 'static')
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
    os.path.join(os.path.dirname(__file__), 'templates'),
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
    'south',
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
]

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'stores.context_processors.site',
    'stores.context_processors.pending_admin',
)

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

    def custom_show_toolbar(request):
        return True # Always show toolbar, for example purposes only.

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
        'EXTRA_SIGNALS': [],
        'HIDE_DJANGO_SQL': True,
        'TAG': 'div',
        'ENABLE_STACKTRACES' : True,
    }

ROOT_URLCONF = 'vapemap.urls'
WSGI_APPLICATION = 'vapemap.wsgi.application'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'strm': sys.stdout
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        '*': {
            'handlers': ['console'],
            'level': 'ERROR',
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
