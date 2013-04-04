from django.test import TestCase
from django.core.urlresolvers import reverse
from stores.models import Chain, Store

class StoreViewsTestCase(TestCase):
    fixtures = ['test_stores']

    def setUp(self):
        self.store = Store.objects.get(pk=3)
        self.chain = Chain.objects.get(pk=1)

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
        resp = self.client.get(reverse('chain-claim', args=[self.chain.slug]))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('chain-claim', args=['test-invalid']))
        self.assertEqual(resp.status_code, 404)

    def test_chain_detail(self):
        resp = self.client.get(reverse('chain-detail', args=[self.chain.slug]))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('chain-detail', args=['test-invalid']))
        self.assertEqual(resp.status_code, 404)

    def test_store_claim(self):
        resp = self.client.get(reverse('store-claim', args=[self.store.slug]))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('store-claim', args=['test-invalid']))
        self.assertEqual(resp.status_code, 200)

    def test_store_update(self):
        resp = self.client.get(reverse('store-update', args=[self.store.slug]))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('store-update', args=['test-invalid']))
        self.assertEqual(resp.status_code, 404)

    def test_store_detail(self):
        resp = self.client.get(reverse('store-detail', args=[self.store.slug]))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('store-detail', args=['test-invalid']))
        self.assertEqual(resp.status_code, 404)