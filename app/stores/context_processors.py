from django.contrib.sites.models import Site
from .models import ClaimRequest, Store

def site(request):
    return {
        'site': Site.objects.get_current()
    }


def pending_admin(request):
    if request.user.is_superuser:
        inactive_stores = Store.objects.filter(active=False).count()
        pending_claims = ClaimRequest.objects.filter(status=ClaimRequest.CLAIM_STATUS_PENDING).count()
        return {
            'admin_pending_claims': pending_claims,
            'admin_inactive_stores': inactive_stores,
        }
    return {}