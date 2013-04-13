from django.forms.models import model_to_dict
from tastypie.resources import ModelResource
from stores.models import County, Country


class CountryResource(ModelResource):

    def dehydrate(self, bundle):
        counties = County.objects.filter(country=bundle.data['id'])
        bundle.data['counties'] = [model_to_dict(c) for c in counties]
        return bundle

    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        filtering = {
            'id': ('exact',)
        }
