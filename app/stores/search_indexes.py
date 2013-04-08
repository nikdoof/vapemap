from haystack import indexes
from .models import Store


class StoreIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    address = indexes.CharField(model_attr='get_full_address')
    location = indexes.LocationField(model_attr='get_location')

    def get_model(self):
        return Store

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(active=True).exclude(address__geo_latitude=None)
