from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django import forms
from django.db import transaction
from django.db.models import Count
from django.utils.timezone import now
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericStackedInline
from .models import Chain, Store, Address, Brand, ClaimRequest, Link, LinkType, County, Country


class LinkInlineAdmin(GenericStackedInline):
    model = Link
    ct_field = 'object_type'


class ChainAdmin(admin.ModelAdmin):
    list_filter = ['active']
    list_display = ['name', 'active', 'changed']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']
    inlines = [
        LinkInlineAdmin,
    ]


class StoreAdmin(admin.ModelAdmin):
    list_filter = ['chain', 'active']
    list_display = ['name', 'store_type', 'active', 'changed']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']
    inlines = [
        LinkInlineAdmin,
    ]
    actions = ['set_active', 'add_brand', 'set_chain']

    class AddBrandForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        brand = forms.ModelChoiceField(Brand.objects)

    def set_active(self, request, queryset):
        with transaction.commit_on_success():
            queryset.update(active=True, changed=now())
        self.message_user(request, "Successfully set %d stores to active." % queryset.count())
    set_active.short_description = 'Set selected stores active.'

    def add_brand(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = self.AddBrandForm(request.POST)
            if form.is_valid():
                count = queryset.count()
                brand = form.cleaned_data['brand']
                with transaction.commit_on_success():
                    for store in queryset:
                        store.brands.add(brand)
                    queryset.update(changed=now())
                if count > 1:
                    plural = 's'
                else:
                    plural = ''
                self.message_user(request, "Successfully added %s to %d store%s." % (brand, count, plural))
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.AddBrandForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        return render_to_response('admin/add_brand.html', {'stores': queryset, 'brand_form': form},
                                  RequestContext(request))

    add_brand.short_description = "Add brand to the selected stores"

    class SetChainForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        chain = forms.ModelChoiceField(Chain.objects)

    def set_chain(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = self.SetChainForm(request.POST)
            if form.is_valid():
                count = queryset.count()
                chain = form.cleaned_data['chain']
                with transaction.commit_on_success():
                    queryset.update(chain=chain, changed=now())
                if count > 1:
                    plural = 's'
                else:
                    plural = ''
                self.message_user(request, "Successfully set %d store%s to %s." % (count, plural, chain))
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.SetChainForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        return render_to_response('admin/set_chain.html', {'stores': queryset, 'chain_form': form},
                                  RequestContext(request))

    set_chain.short_description = "Set the selected store's chain"


class ClaimAdmin(admin.ModelAdmin):
    list_filter = ['status']
    list_display = ['generic_obj', 'user', 'status', 'note']
    actions = ['approve_request']

    def approve_request(self, request, queryset):
        qs = queryset.filter(status=ClaimRequest.CLAIM_STATUS_PENDING)
        with transaction.commit_on_success():
            for obj in qs:
                obj.status = ClaimRequest.CLAIM_STATUS_APPROVED
                target = obj.generic_obj
                target.editor = obj.user
                target.save()
                obj.save()
        if qs.count() == 1:
            message_bit = "1 request was"
        else:
            message_bit = "%s requests were" % qs.count()
        self.message_user(request, "%s successfully approved." % message_bit)

    approve_request.short_description = 'Approve selected requests.'


class CountyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'country', 'address_count']
    actions = ['set_country']

    def address_count(self, obj):
        return obj.address_count
    address_count.admin_order_field = 'address_count'

    def queryset(self, request):
        qs = super(CountyAdmin, self).queryset(request)
        return qs.annotate(address_count=Count('addresses'))

    class SetCountryForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        country = forms.ModelChoiceField(Country.objects)

    def set_country(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = self.SetCountryForm(request.POST)
            if form.is_valid():
                country = form.cleaned_data['country']
                with transaction.commit_on_success():
                    queryset.update(country=country)
                self.message_user(request, "Successfully set %d counties to %s." % (queryset.count(), country))
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.SetCountryForm(initial={'_selected_action': queryset.values_list('id', flat=True)})
        return render_to_response('admin/set_country.html', {'stores': queryset, 'country_form': form},
                                  RequestContext(request))

    set_country.short_description = "Set the selected county's country"


class CountryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'address_count', 'county_count']

    def address_count(self, obj):
        return obj.address_count
    address_count.admin_order_field = 'address_count'

    def county_count(self, obj):
        return obj.county_count
    county_count.admin_order_field = 'county_count'

    def queryset(self, request):
        qs = super(CountryAdmin, self).queryset(request)
        return qs.annotate(address_count=Count('addresses'), county_count=Count('counties'))


admin.site.register(Chain, ChainAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Address, admin.ModelAdmin)
admin.site.register(Brand, admin.ModelAdmin)
admin.site.register(ClaimRequest, ClaimAdmin)
admin.site.register(LinkType, admin.ModelAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(Country, CountryAdmin)