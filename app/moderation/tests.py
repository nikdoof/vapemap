"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import json
from django.test import TestCase
from django.core.urlresolvers import reverse
try:
    from django.contrib.auth import get_user_model
    USER_MODEL = get_user_model()
except ImportError:
    from django.contrib.auth.models import User as USER_MODEL
from moderation.models import FlagType, FlaggedObject


class FlagObjectViewTestCase(TestCase):

    def setUp(self):
        self.u1 = USER_MODEL.objects.create_user('user1', 'test@test.com', 'user1')
        self.f1 = FlagType.objects.create(name='Test')

    def tearDown(self):
        self.u1.delete()
        self.f1.delete()

    def post_to_flagobject(self, data={}):
        return self.client.post(reverse('moderation_flagobject'), data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')


    def test_invalid_json(self):
        resp = self.post_to_flagobject('')
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEqual(content['result'], 'invalid-request')
        self.assertEqual(content['reason'], 'invalid-request')

    def test_invalid_json_2(self):
        resp = self.post_to_flagobject({'data': '1234567890'})
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEqual(content['result'], 'invalid-request')
        self.assertEqual(content['reason'], 'invalid-json')

    def test_missing_app_model_json(self):
        resp = self.post_to_flagobject(json.dumps({'invalid': 'invalid'}))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEqual(content['result'], 'invalid-request')
        self.assertEqual(content['reason'], 'no-app-or-model')

    def test_unknown_type(self):
        resp = self.post_to_flagobject(json.dumps({
            'app': 'moderation',
            'model': 'xxxxxxxxxxxxxxxxxxxx',
            'id': 999999,
            'flag_type': 1,
            'note': 'test note',
        }))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEqual(content['result'], 'invalid-request')
        self.assertEqual(content['reason'], 'unknown-object-type')

    def test_missing_object(self):
        resp = self.post_to_flagobject(json.dumps({
                'app': 'moderation',
                'model': 'flaggedobject',
                'id': 999999,
                'flag_type': 1,
                'note': 'test note',
        }))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEqual(content['result'], 'invalid-request')
        self.assertEqual(content['reason'], 'does-not-exist')

    def test_missing_fields(self):
        resp = self.post_to_flagobject(json.dumps({
            'app': 'moderation',
            'model': 'flaggedobject',
            'id': 999999,
            'flag_type': 1,
            }))
        self.assertEqual(resp.status_code, 400)
        content = json.loads(resp.content)
        self.assertEqual(content['result'], 'invalid-request')
        self.assertEqual(content['reason'], 'missing-fields')

    def test_flagging_authenticated(self):

        self.client.login(username='user1', password='user1')

        resp = self.post_to_flagobject(json.dumps({
            'app': 'moderation',
            'model': 'flagtype',
            'id': self.f1.pk,
            'flag_type': 1,
            'note': 'test note',
        }))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['result'], 'ok')
        self.assertIsNotNone(content['flag_id'])

        flag = FlaggedObject.objects.get(pk=content['flag_id'])
        self.assertIsNotNone(flag)
        self.assertEqual(flag.user, self.u1)
        self.assertEqual(flag.flag_type, self.f1)

    def test_flagging_unauthenticated(self):

        self.client.logout()

        resp = self.post_to_flagobject(json.dumps({
            'app': 'moderation',
            'model': 'flagtype',
            'id': self.f1.pk,
            'flag_type': 1,
            'note': 'test note',
            }))
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertEqual(content['result'], 'ok')
        self.assertIsNotNone(content['flag_id'])

        flag = FlaggedObject.objects.get(pk=content['flag_id'])
        self.assertIsNotNone(flag)
        self.assertEqual(flag.user, None)
        self.assertEqual(flag.flag_type, self.f1)