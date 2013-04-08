from django.views.generic import ListView
from ..models import Brand


class BrandListView(ListView):
    model = Brand
    paginate_by = 10

    def get_queryset(self):
        qs = super(BrandListView, self).get_queryset()
        return qs.exclude(stores=None).prefetch_related('stores')
