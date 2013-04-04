from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from ..forms import ClaimRequestForm
from ..models import ClaimRequest
from .mixins import WaffleSwitchMixin


class ClaimCreateView(WaffleSwitchMixin, CreateView):
    model = ClaimRequest
    target_model = None
    form_class = ClaimRequestForm
    template_name = 'stores/claim_form.html'
    waffle_switch = 'claim_support'

    def get(self, request, *args, **kwargs):
        self.target_obj = self.get_target_object()
        if not self.target_obj:
            raise Http404
        return super(ClaimCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.target_obj = self.get_target_object()
        return super(ClaimCreateView, self).post(request, *args, **kwargs)

    def get_target_object(self):
        obj_slug = self.kwargs.get('slug')
        try:
            obj = self.target_model.objects.get(slug=obj_slug)
        except self.target_model.DoesNotExist:
            return None
        return obj

    def get_context_data(self, **kwargs):
        ctx = super(ClaimCreateView, self).get_context_data(**kwargs)
        ctx.update({
            'target_obj': self.target_obj,
        })
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.object_id = self.target_obj.pk
        obj.object_type = ContentType.objects.get_for_model(self.target_model)
        obj.user = self.request.user
        obj.save()
        messages.success(self.request, 'Your claim request for %s has been successfully submitted for review.' % self.target_obj)
        return super(ClaimCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('store-detail', args=[self.target_obj.slug])