import csv
import requests
from StringIO import StringIO
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from stores.models import Country, County, Address, Store


class Command(BaseCommand):
    args = '<file or url>'
    help = 'Import a list of stores from CSV'

    def handle(self, *args, **options):
        file = args[0]
        if file.startswith('http'):
            self.stdout.write("Downloading %s\n" % file)
            f = StringIO(requests.get(file).text)
        else:
            self.stdout.write("Opening file %s\n" % file)
            f = open(file, 'r')

        for row in csv.reader(f):
            row = [x.strip() for x in row]
            name, addr1, addr2, addr3, city, county, country, postcode, email, website, phone, y, x, twitter, facebook, facebook2 = row
            self.stdout.write("Importing %s... " % name)
            try:
                obj = Store.objects.get(name=name)
            except Store.DoesNotExist:
                pass
            else:
                if obj.address.postcode == postcode:
                    self.stdout.write("Store by that name already exists, skipping.\n")
                    continue
            with transaction.commit_on_success():
                country, created = Country.objects.get_or_create(name=country)
                county, created = County.objects.get_or_create(name=county, country=country)
                addr = Address(name=name, address1=addr1, address2=addr2, address3=addr3, city=city, county=county, country=country, postcode=postcode, geo_latitude=y, geo_longitude=x)
                addr.save()
                store = Store(name=name, address=addr, website=website, email=email, phone=phone)
                if website:
                    store.store_type = Store.STORE_TYPE_BOTH
                store.save()
            self.stdout.write("Done\n")

        f.close()
        self.stdout.write("Done\n")
