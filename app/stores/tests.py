from django.test import TestCase
from django.core.urlresolvers import reverse
from stores.models import Chain, Store, Address, Country
from waffle import Switch


class StoresViewsTestCase(TestCase):
    """
    Tests that all basic views return expected results without in-depth checking.
    """
    fixtures = ['test_stores']

    def setUp(self):
        self.store = Store.objects.get(pk=3)
        self.chain = Chain.objects.get(pk=1)

        # Enable claim support for the tests
        Switch.objects.filter(name='claim_support').update(active=True)

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
        self.assertEqual(resp.status_code, 404)

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


class StoresUtilsTestCase(TestCase):

    def test_caching_geo_lookup(self):
        from stores.utils import caching_geo_lookup
        from django.core.cache import cache
        addr = "Bridge Street, Warrington, WA3"
        slug = addr.lower().replace(',', '').replace(' ', '-')
        print slug
        lat, lng = caching_geo_lookup(addr)
        self.assertNotEqual(lat, '')
        self.assertNotEqual(lng, '')
        self.assertIsNotNone(cache.get('geo_%s' % slug, None))


class StoresChainModelTestCase(TestCase):
    """
    Basic tests against the Chain model
    """

    def test_slug_creation(self):
        obj = Chain(name='Test Chain 1')
        obj.save()
        self.assertEqual(obj.slug, 'test-chain-1')

    def test_absolute_url(self):
        obj = Chain(name='Test Chain 2')
        obj.save()
        self.assertEqual(str(obj.get_absolute_url()), '/chains/test-chain-2/')

    def test_chain_name(self):
        obj = Chain(name='Test Chain 3')
        self.assertEqual(str(obj), 'Test Chain 3')


class StoresStoreModelTestCase(TestCase):
    """
    Basic tests against the Store model
    """
    fixtures = ['countries']

    def setUp(self):
        country = Country.objects.get(name='United Kingdom')
        self.addr = Address(name='test', address1='Bridge Street', city='Warrington', country=country, postcode='WA3')
        self.addr.save()

    def test_slug_creation(self):
        obj = Store(name='Test Store 1', address=self.addr)
        obj.save()
        self.assertEqual(obj.slug, 'test-store-1')

    def test_absolute_url(self):
        obj = Store(name='Test Store 2', address=self.addr)
        obj.save()
        self.assertEqual(str(obj.get_absolute_url()), '/stores/test-store-2/')

    def test_chain_name(self):
        obj = Store(name='Test Store 3', address=self.addr)
        self.assertEqual(str(obj), 'Test Store 3')


class StoresAddressModelTestCase(TestCase):

    fixtures = ['countries']

    def test_geo_lookup(self):
        country = Country.objects.get(name='United Kingdom')
        addr = Address(name='test', address1='Bridge Street', city='Warrington', country=country, postcode='WA3')
        addr.save()
        self.assertIsNotNone(addr.geo_latitude)
        self.assertIsNotNone(addr.geo_longitude)

    def test_skip_geo_lookup(self):
        country = Country.objects.get(name='United Kingdom')
        addr = Address(name='test', address1='Bridge Street', city='Warrington', country=country, postcode='WA3')
        addr.save(no_lookup=True)
        self.assertIsNone(addr.geo_latitude)
        self.assertIsNone(addr.geo_longitude)