from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from tastypie.api import Api
from stores.api import CountryResource, CountyResource
admin.autodiscover()


v1_api = Api(api_name='1.0')
v1_api.register(CountryResource())


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'user/', include('registration.backends.default.urls')),
    url(r'user/', include('django.contrib.auth.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^moderation/', include('moderation.urls')),
    url(r'^api/', include(v1_api.urls)),
    url('', include('stores.urls'))
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^500/$', 'django.views.defaults.server_error'),
    )
