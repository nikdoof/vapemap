from django.contrib.sites.models import Site
from moderation.models import FlaggedObject

def pending_flagged_admin(request):
    if request.user.is_superuser:
        pending_flags = FlaggedObject.objects.filter(status=1).count()
        return {
            'admin_pending_flags': pending_flags
        }
    return {}
