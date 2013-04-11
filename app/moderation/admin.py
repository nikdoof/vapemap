from django.contrib import admin
from moderation.models import FlagType, FlaggedObject


class FlaggedObjectModelAdmin(admin.ModelAdmin):
    list_display = ['generic_obj', 'user', 'status', 'note']
    list_filter = ['status']


admin.site.register(FlagType, admin.ModelAdmin)
admin.site.register(FlaggedObject, FlaggedObjectModelAdmin)
