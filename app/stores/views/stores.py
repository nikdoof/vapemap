from django.views.generic import ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.formtools.wizard.views import SessionWizardView
from .mixins import EditorCheckMixin, HaystackSearchListMixin
from ..forms import StoreForm, AddressForm
from ..models import Store, Brand


class StoreListView(HaystackSearchListMixin, ListView):
    model = Store
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ctx = super(StoreListView, self).get_context_data(**kwargs)

        search = self.get_search_terms()
        if search:
            ctx.update({
                'search_query': search,
            })
        return ctx

    def get_queryset(self):
        qs = super(StoreListView, self).get_queryset()
        return qs.filter(active=True).select_related('address', 'address__country')


class OnlineStoreListView(StoreListView):
    template_name_suffix = '_online_list'

    def get_queryset(self):
        qs = super(OnlineStoreListView, self).get_queryset()
        return qs.filter(store_type__in=[Store.STORE_TYPE_ONLINE, Store.STORE_TYPE_BOTH])


class RetailStoreListView(StoreListView):
    template_name_suffix = '_retail_list'

    def get_queryset(self):
        qs = super(RetailStoreListView, self).get_queryset()
        return qs.filter(store_type__in=[Store.STORE_TYPE_RETAIL, Store.STORE_TYPE_BOTH])


class StockistStoreListView(StoreListView):
    template_name_suffix = '_stockist_list'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.brand = Brand.objects.get(name=kwargs.pop('brand', None))
        except Brand.DoesNotExist:
            raise Http404
        return super(StockistStoreListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(StockistStoreListView, self).get_context_data(**kwargs)
        ctx.update({
            'brand': self.brand,
        })
        return ctx

    def get_queryset(self):
        qs = super(StockistStoreListView, self).get_queryset()
        return qs.filter(brands__in=[self.brand])


class StoreDetailView(EditorCheckMixin, DetailView):
    model = Store

    def get_queryset(self):
        qs = super(StoreDetailView, self).get_queryset()
        return qs.filter(active=True).select_related('address', 'address__county', 'address__country', 'chain')\
            .prefetch_related('brands')


class StoreUpdateView(UpdateView):
    model = Store
    form_class = StoreForm

    def form_valid(self, form):
        messages.success(self.request, "%s updated successfully." % self.object)
        return super(UpdateView, self).form_valid(form)


class StoreCreateView(SessionWizardView):
    form_list = [AddressForm, StoreForm]

    def done(self, form_list, **kwargs):

        address, store = form_list

        addr_obj = address.save(commit=False)
        store_obj = store.save(commit=False)

        addr_obj.name = store_obj.name
        addr_obj.save()
        store_obj.address = addr_obj
        store_obj.active = False
        store_obj.save()

        messages.success(self.request, "%s has been sumbitted for moderation and should be visible within the "
                                       "next 24 hours." % store_obj)

        return HttpResponseRedirect(reverse('map'))

    def get_template_names(self):
        return 'stores/wizard/store_wizard.html'