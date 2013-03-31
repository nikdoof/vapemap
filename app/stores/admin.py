from django.contrib import admin
from .models import Chain, Store, Address, Brand, ClaimRequest


class ChainAdmin(admin.ModelAdmin):
    list_filter = ['active']
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class StoreAdmin(admin.ModelAdmin):
    list_filter = ['chain', 'active']
    list_display = ['name', 'store_type', 'active']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name']


class ClaimAdmin(admin.ModelAdmin):
    list_filter = ['status']
    list_display = ['generic_obj', 'user', 'status', 'note']
    actions = ['approve_request']


    def approve_request(self, request, queryset):
        qs = queryset.filter(status=ClaimRequest.CLAIM_STATUS_PENDING)
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


admin.site.register(Chain, ChainAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Address, admin.ModelAdmin)
admin.site.register(Brand, admin.ModelAdmin)
admin.site.register(ClaimRequest, ClaimAdmin)