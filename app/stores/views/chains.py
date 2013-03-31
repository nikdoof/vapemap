from django.views.generic import ListView, DetailView
from .mixins import EditorCheckMixin
from ..models import Chain


class ChainListView(ListView):
    model = Chain
    paginate_by = 10

    def get_queryset(self):
        qs = super(ChainListView, self).get_queryset()
        return qs.filter(active=True).prefetch_related('stores')


class ChainDetailView(EditorCheckMixin, DetailView):
    model = Chain

    def get_queryset(self):
        qs = super(ChainDetailView, self).get_queryset()
        return qs.filter(active=True).prefetch_related('stores', 'stores__address')