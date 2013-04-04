from .base import *


INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

def custom_show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'EXTRA_SIGNALS': [],
    'HIDE_DJANGO_SQL': True,
    'TAG': 'div',
    'ENABLE_STACKTRACES' : True,
}
