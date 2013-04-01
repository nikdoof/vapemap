from django.http import Http404
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery
from waffle import switch_is_active, flag_is_active


class WaffleSwitchMixin(object):
    """
    Checks that as switch is active, or 404. Operates like the FBV decorator waffle_switch
    """
    waffle_switch = None

    def dispatch(self, request, *args, **kwargs):
        if self.waffle_switch.startswith('!'):
            active = not switch_is_active(self.waffle_switch[1:])
        else:
            active = switch_is_active(self.waffle_switch)

        if not active:
            raise Http404
        return super(WaffleSwitchMixin, self).dispatch(request, *args, **kwargs)


class WaffleFlagMixin(object):
    """
    Checks that as flag is active, or 404. Operates like the FBV decorator waffle_flag
    """
    waffle_flag = None

    def dispatch(self, request, *args, **kwargs):
        if self.waffle_flag.startswith('!'):
            active = not flag_is_active(request, self.waffle_flag[1:])
        else:
            active = flag_is_active(request, self.waffle_flag)

        if not active:
            raise Http404
        return super(WaffleFlagMixin, self).dispatch(request, *args, **kwargs)


class EditorCheckMixin(object):
    """
    A mixin to check if the object is inactive to only show it to editors or superusers
    """

    def is_editor(self, object):
        if self.request.user.is_superuser or self.request.user == object.editor:
            return True
        return False

    def get_object(self, queryset=None):
        obj = super(EditorCheckMixin, self).get_object(queryset)
        if not obj.active:
            if not self.is_editor(obj):
                raise Http404
        return obj

    def get_context_data(self, **kwargs):
        ctx = super(EditorCheckMixin, self).get_context_data(**kwargs)
        ctx.update({
            'is_editor': self.is_editor(self.object)
        })
        return ctx


class HaystackSearchListMixin(object):
    """
    Adds searching via Haystack to a regular ListView
    """

    search_parameter = 'q'

    def get_search_terms(self):
        return self.request.GET.get(self.search_parameter, None)

    def get_search_filter(self):
        return {
            'content': AutoQuery(self.get_search_terms())
        }

    def haystack_search(self):
        return SearchQuerySet().filter(**self.get_search_filter()).models(self.model)

    def get_queryset(self):
        if self.get_search_terms():
            res = self.haystack_search()
            if res.count() == 0:
                return self.model.objects.none()
            return self.model.objects.filter(pk__in=[r.object.pk for r in res.load_all()])
        else:
            return super(HaystackSearchListMixin, self).get_queryset()