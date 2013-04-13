import csv
import requests
from StringIO import StringIO
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from stores.models import Country, County, Address, Store, Link, LinkType
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    args = '<file or url>'
    help = 'Import a list of stores from CSV'

    def handle(self, *args, **options):
        fn = args[0]
        if fn.startswith('http'):
            self.stdout.write("Downloading %s\n" % fn)
            f = StringIO(requests.get(fn).text)
        else:
            self.stdout.write("Opening file %s\n" % fn)
            f = open(fn, 'r')

        self.stdout.write('Formatting data...')
        # Generate the dataset
        reader = csv.reader(f)
        headers = [h.lower().strip() for h in reader.next()]
        data = []
        for row in reader:
            values = []
            for h, v in zip(headers, row):
                if v == '':
                    value = None
                else:
                    value = v.strip()
                values.append((h, value))
            data.append(dict(values))

        self.stdout.write('%d entries found.' % len(data))
        for row in data:
            self.stdout.write("Importing %s... " % row['name'])
            try:
                obj = Store.objects.get(name=row['name'])
            except Store.DoesNotExist:
                pass
            else:
                if obj.address.postcode == row['postcode']:
                    self.stdout.write("Store by that name already exists, skipping.\n")
                    continue
            with transaction.commit_on_success():
                if not row['country']:
                    row['country'] = 'United Kingdom'
                country, created = Country.objects.get_or_create(name=row['country'])
                county, created = County.objects.get_or_create(name=row['county'], country=country)
                addr = Address(name=row['name'], address1=row['address1'], address2=row['address2'],
                               address3=row['address3'], city=row['city'], county=county, country=country,
                               postcode=row['postcode'], geo_latitude=row['y'], geo_longitude=row['x'])
                addr.save(no_lookup=True)
                store = Store(name=row['name'], address=addr, website=row['website'], email=row['email'],
                              phone=row['phone'])
                if row['type']:
                    if row['type'] == 'Online':
                        store.store_type = Store.STORE_TYPE_ONLINE
                    if row['type'] == 'Retail':
                        store.store_type = Store.STORE_TYPE_RETAIL
                    if row['type'] == 'Both':
                        store.store_type = Store.STORE_TYPE_BOTH
                elif row['website']:
                    store.store_type = Store.STORE_TYPE_BOTH
                store.save()
                if row['twitter']:
                    Link(object_id=store.pk, object_type=ContentType.objects.get_for_model(store.__class__),
                         account_type=LinkType.objects.get(name='Twitter'),
                         account_name=row['twitter'].split('/')[-1]).save()
            self.stdout.write("Done\n")

        f.close()
        self.stdout.write("Done\n")
