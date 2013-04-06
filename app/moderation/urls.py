from django.conf.urls import patterns, url
from moderation.views import FlagObjectView

urlpatterns = patterns('',
    url(r'^flag/$', FlagObjectView.as_view(), name='moderation_flagobject'),
)