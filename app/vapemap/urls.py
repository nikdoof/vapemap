from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'user/', include('registration.backends.default.urls')),
    url(r'user/', include('django.contrib.auth.urls')),
    url(r'^search/', include('haystack.urls')),
    url('', include('stores.urls'))
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^500/$', 'django.views.defaults.server_error'),
    )
