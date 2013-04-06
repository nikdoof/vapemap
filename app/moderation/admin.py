from django.contrib import admin
from moderation.models import FlagType, FlaggedObject

admin.site.register(FlagType, admin.ModelAdmin)
admin.site.register(FlaggedObject, admin.ModelAdmin)
