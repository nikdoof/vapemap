from django.contrib.sites.models import Site
from .models import ClaimRequest

def site(request):
    return {
        'site': Site.objects.get_current()
    }


def pending_admin(request):
    if request.user.is_superuser:
        pending = ClaimRequest.objects.filter(status=ClaimRequest.CLAIM_STATUS_PENDING).count()
        return {
            'admin_pending_requests': pending
        }
    return {}