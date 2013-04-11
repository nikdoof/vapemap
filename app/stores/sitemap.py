from django.contrib.sitemaps import Sitemap
from stores.models import Store, Chain


class StoreSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1

    def items(self):
        return Chain.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.changed


class ChainSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return Store.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.changed


sitemaps = {
    'stores': StoreSitemap,
    'chains': ChainSitemap,
}