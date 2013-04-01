from django.views.generic import ListView
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point, D
from ..models import Store
from ..utils import caching_geo_lookup


class DistanceSearchView(ListView):

    template_name = 'stores/store_search.html'
    distance = 25

    def get_location(self):
        # TODO: geopy the location based on kwargs
        location = self.request.GET.get('location')
        lat = self.request.GET.get('lat')
        lng = self.request.GET.get('lng')
        if location:
            name, geo = caching_geo_lookup(location)
        elif lat and lng:
            geo = (lat, lng)
        else:
            geo = None
        self.location_geo = geo

        return Point(geo[1], geo[0])

    def get_distance(self):
        return D(km=self.request.GET.get('distance', self.distance))

    def get_queryset(self):
        location = self.get_location()
        if not location:
            return SearchQuerySet.none
        distance = self.get_distance()
        print location, distance
        return SearchQuerySet().dwithin('location', location, distance).distance('location', location).order_by('-distance')

    def get_context_data(self, **kwargs):
        ctx = super(DistanceSearchView, self).get_context_data(**kwargs)
        ctx.update({
            'location': self.request.GET.get('location'),
            'location_geo': self.location_geo,
        })
        return ctx