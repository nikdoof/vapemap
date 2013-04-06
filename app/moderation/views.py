import json
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.contrib.contenttypes.models import ContentType
from braces.views import AjaxResponseMixin, JSONResponseMixin
from moderation.models import FlaggedObject


class FlagObjectView(JSONResponseMixin, AjaxResponseMixin, View):
    """
    Ajax capable view to flag a object for moderation
    """

    def render_invalid_response(self, reason='invalid-request'):
        return HttpResponseBadRequest(content=json.dumps({
            'result': 'invalid-request',
            'reason': reason,
        }), content_type=self.get_content_type())

    def post(self, request, *args, **kwargs):
        pass

    def post_ajax(self, request, *args, **kwargs):
        data = request.raw_post_data
        if not data:
            return self.render_invalid_response()
        try:
            data = json.loads(data)
        except ValueError:
            return self.render_invalid_response('invalid-json')
        if not isinstance(data, dict):
            return self.render_invalid_response('invalid-json')
        if not 'app' in data or not 'model' in data:
            return self.render_invalid_response('no-app-or-model')
        if not 'flag_type' in data or not 'note' in data:
            return self.render_invalid_response('missing-fields')
        try:
            ct = ContentType.objects.get(app_label=data['app'], model=data['model'])
        except ContentType.DoesNotExist:
            return self.render_invalid_response('unknown-object-type')
        cls = ct.model_class()
        try:
            cls.objects.get(pk=data['id'])
        except cls.DoesNotExist:
            return self.render_invalid_response('does-not-exist')
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        flag = FlaggedObject(object_type=ct, object_id=data['id'], flag_type_id=data['flag_type'],
                             note=data['note'], user=user)
        flag.save()
        result = {
            'result': 'ok',
            'flag_id': flag.pk,
        }
        return self.render_json_response(result)