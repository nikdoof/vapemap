from django.core.cache import cache
from geopy.geocoders import GoogleV3
from geopy.geocoders.base import GeocoderResultError


def caching_geo_lookup(address):
    """
    Preforms a geo lookup against Google V3 and caches the results
    """
    if not address:
        return None
    slug = address.lower().replace(',', '').replace(' ', '-')
    geo = cache.get('geo_%s' % slug)
    if not geo:
        try:
            geo = GoogleV3().geocode(address)
        except GeocoderResultError:
            return None
        cache.set('geo_%s' % slug, geo, 3600)
    return geo