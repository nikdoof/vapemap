from django.test import TestCase
from django.core.urlresolvers import reverse


class StoreViewsTestCase(TestCase):

    def test_map_index(self):
        resp = self.client.get(reverse('map'))
        self.assertEqual(resp.status_code, 200)

    def test_store_list(self):
        resp = self.client.get(reverse('store-list'))
        self.assertEqual(resp.status_code, 200)

    def test_chain_list(self):
        resp = self.client.get(reverse('chain-list'))
        self.assertEqual(resp.status_code, 200)

    def test_chain_claim(self):
        resp = self.client.get(reverse('chain-claim'))
        self.assertEqual(resp.status_code, 200)

    def test_store_claim(self):
        resp = self.client.get(reverse('store-claim'))
        self.assertEqual(resp.status_code, 200)

    def test_store_update(self):
        resp = self.client.get(reverse('store-update'))
        self.assertEqual(resp.status_code, 200)