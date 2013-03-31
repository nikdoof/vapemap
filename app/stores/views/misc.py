from django.core.cache import cache
from django.views.generic import ListView
from ..models import Chain, Store


class MapView(ListView):
    model = Store
    template_name_suffix = '_map'

    def get_context_data(self, **kwargs):
        ctx = super(MapView, self).get_context_data(**kwargs)

        stores = cache.get('store_count')
        chains = cache.get('chain_count')

        if not stores:
            stores = Store.objects.filter(active=True).count()
            cache.set('store_count', stores, 600)

        if not chains:
            chains = Chain.objects.filter(active=True).count()
            cache.set('chain_count', chains, 600)

        ctx.update({
            'store_count': stores,
            'chain_count': chains,
            })
        return ctx

    def get_queryset(self):
        qs = super(MapView, self).get_queryset()
        return qs.filter(active=True).select_related('address')
