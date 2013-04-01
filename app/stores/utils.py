from math import radians, cos, sin, asin, sqrt
from django.core.cache import cache
from geopy.geocoders import GoogleV3
from geopy.geocoders.base import GeocoderResultError


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


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