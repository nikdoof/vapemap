from django.conf.urls import patterns, include, url
from .views import *
from .forms import AddressForm, StoreForm
from .models import Store, Chain

urlpatterns = patterns('',
    url(r'^$', MapView.as_view(), name='map'),

    url(r'^chains/$', ChainListView.as_view(), name='chain-list'),
    url(r'^chains/(?P<slug>.*)/claim/$', ClaimCreateView.as_view(target_model=Chain), name='chain-claim'),
    url(r'^chains/(?P<pk>\d+)/$', ChainDetailView.as_view(), name='chain-detail-pk'),
    url(r'^chains/(?P<slug>.*)/$', ChainDetailView.as_view(), name='chain-detail'),

    url(r'^stores/$', StoreListView.as_view(), name='store-list'),
    url(r'^stores/create/$', StoreCreateView.as_view([AddressForm, StoreForm]), name='store-create'),
    url(r'^stores/search/$', DistanceSearchView.as_view(), name='store-search'),
    url(r'^stores/(?P<slug>.*)/claim/$', ClaimCreateView.as_view(target_model=Store), name='store-claim'),
    url(r'^stores/(?P<slug>.*)/update/$', StoreUpdateView.as_view(), name='store-update'),
    url(r'^stores/(?P<pk>\d+)/$', StoreDetailView.as_view(), name='store-detail-pk'),
    url(r'^stores/(?P<slug>.*)/$', StoreDetailView.as_view(), name='store-detail'),

)