import re
from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from stores.utils import caching_geo_lookup

USER_MODEL = get_user_model()


class Chain(models.Model):
    name = models.CharField('Name', max_length=200)
    slug = models.SlugField('URL Slug', max_length=200, blank=True)
    head_office = models.ForeignKey('stores.Address', blank=True, null=True)
    website = models.URLField('Website', blank=True, null=True)
    editor = models.ForeignKey(USER_MODEL, related_name='editable_chains', blank=True, null=True)
    active = models.BooleanField('Active?', default=True)

    long_description = models.TextField('Description', null=True, blank=True)
    links = generic.GenericRelation('stores.Link', content_type_field='object_type')

    created = models.DateTimeField('Created Date/Time', default=now)
    changed = models.DateTimeField('Changed Date/Time', default=now)

    def save(self, **kwargs):
        if self.slug == '':
            self.slug = re.sub(r'\W+', '-', str(self.name).lower())
        self.changed = now()
        return super(Chain, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse_lazy('chain-detail', args=[self.slug])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'stores'


class Store(models.Model):

    STORE_TYPE_RETAIL = 1
    STORE_TYPE_ONLINE = 2
    STORE_TYPE_BOTH = 3

    STORE_TYPE_CHOICES = (
        (STORE_TYPE_RETAIL, 'Retail Only'),
        (STORE_TYPE_ONLINE, 'Online Only'),
        (STORE_TYPE_BOTH, 'Retail & Online'),
    )

    name = models.CharField('Name', max_length=200, help_text="Store's full name")
    slug = models.SlugField('URL Slug', max_length=200, blank=True)
    address = models.ForeignKey('stores.Address', related_name='stores')
    store_type = models.IntegerField('Store Type', choices=STORE_TYPE_CHOICES, default=STORE_TYPE_RETAIL)
    chain = models.ForeignKey(Chain, related_name='stores', null=True, blank=True)
    editor = models.ForeignKey(USER_MODEL, related_name='editable_stores', null=True, blank=True)
    active = models.BooleanField('Active?', default=True)

    website = website = models.URLField('Website', null=True, blank=True)
    email = models.EmailField('Email', null=True, blank=True, help_text="Contact email address for the store.")
    phone = models.CharField('Phone', max_length=25, null=True, blank=True, help_text="Contact phone number for the store.")
    links = generic.GenericRelation('stores.Link', content_type_field='object_type')

    long_description = models.TextField('Description', null=True, blank=True, help_text="Full description of the store, including any marketing material. Markdown supported.")
    brands = models.ManyToManyField('stores.Brand', related_name='stores', null=True, blank=True, help_text="Brands that are sold by this store.")

    created = models.DateTimeField('Created Date/Time', default=now)
    changed = models.DateTimeField('Changed Date/Time', default=now)

    def get_full_address(self):
        if self.address:
            return self.address.full_address

    def get_location(self):
        if self.address:
            return self.address.geo_location

    def save(self, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = re.sub(r'\W+', '-', str(self.name).lower())
        self.changed = now()
        return super(Store, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse_lazy('store-detail', args=[self.slug])

    def __unicode__(self):
        if not self.name and self.chain:
            return self.chain.name
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'stores'


class Brand(models.Model):
    name = models.CharField('Brand Name', max_length=200)
    website = models.URLField('Brand Website', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'stores'


class County(models.Model):
    """
    UK Counties
    """
    name = models.CharField('Name', max_length=100)
    country = models.ForeignKey('stores.Country', related_name='counties', null=True, blank=True)

    @property
    def stores(self):
        return Store.objects.filter(address__county__pk=self.pk)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'stores'
        verbose_name_plural = 'Counties'


class Country(models.Model):
    """
    ISO Countries
    """
    iso_code = models.CharField('ISO Code', max_length=3)
    name = models.CharField('Name', max_length=100)

    @property
    def stores(self):
        return Store.objects.filter(address__country__pk=self.pk)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'stores'
        verbose_name_plural = 'Countries'


class Address(models.Model):
    """
    Represents a location or postal address
    """
    name = models.CharField('Address Name', max_length=200)
    address1 = models.CharField('Address Line 1', max_length=200, help_text="First line of the address. e.g. <em>1 Station Road</em>")
    address2 = models.CharField('Address Line 2', max_length=200, null=True, blank=True, help_text="(Optional) Second line of the address")
    address3 = models.CharField('Address Line 3', max_length=200, null=True, blank=True, help_text="(Optional) Third line of the address")
    city = models.CharField('Town/City', max_length='50', help_text="City or town")
    county = models.ForeignKey('stores.County', related_name='addresses', null=True, blank=True, help_text="County or suburban area. (Ignore if the store is outside the UK)")
    country = models.ForeignKey('stores.Country', related_name='addresses')
    postcode = models.CharField('Postcode / Zipcode', max_length=20, null=True, blank=True, help_text="Post Code or Zip Code, e.g. <em>M1 1AA</em> or <em>60647</em>")

    geo_latitude = models.FloatField('Latitude', null=True, blank=True)
    geo_longitude = models.FloatField('Longitude', null=True, blank=True)

    @property
    def full_address(self):
        fields = [
            self.address1,
            self.address2,
            self.address3,
            self.city,
            self.county,
            self.postcode,
            self.country.name,
        ]
        return u', '.join([unicode(f).strip() for f in fields if f and unicode(f).strip() != ''])

    @property
    def geo_location(self):
        return Point(self.geo_longitude, self.geo_latitude)

    def __unicode__(self):
        if self.name:
            return self.name
        return self.address_string

    def save(self, **kwargs):
        no_lookup = kwargs.pop('no_lookup', None)
        if not no_lookup and not self.geo_latitude and not self.geo_longitude:
            res = caching_geo_lookup(self.full_address)
            if res:
                self.geo_latitude, self.geo_longitude = res[1]
        return super(Address, self).save(**kwargs)

    class Meta:
        app_label = 'stores'


class ClaimRequest(models.Model):

    CLAIM_STATUS_PENDING = 0
    CLAIM_STATUS_APPROVED = 1
    CLAIM_STATUS_REJECTED = 2

    CLAIM_STATUS_CHOICES = (
        (CLAIM_STATUS_PENDING, 'Pending'),
        (CLAIM_STATUS_APPROVED, 'Approved'),
        (CLAIM_STATUS_REJECTED, 'Rejected')
    )

    object_id = models.PositiveIntegerField()
    object_type = models.ForeignKey(ContentType)
    generic_obj = generic.GenericForeignKey('object_type', 'object_id')

    user = models.ForeignKey(USER_MODEL, related_name='claims')
    note = models.TextField('Claim Note')
    status = models.IntegerField('Status', choices=CLAIM_STATUS_CHOICES, default=CLAIM_STATUS_PENDING)

    class Meta:
        app_label = 'stores'