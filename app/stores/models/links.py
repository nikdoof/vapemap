from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.loader import render_to_string


class LinkType(models.Model):
    """
    Define types of links that can be used on objects
    """
    name = models.CharField('Name', max_length=200)
    icon = models.CharField('Icon', max_length=100, default="icon-globe")
    url_format = models.CharField('URL Format', max_length=255)
    is_active = models.BooleanField('Active?', default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        app_label = 'stores'


class Link(models.Model):
    """
    Represents a link that can be bound to a object
    """
    object_id = models.PositiveIntegerField()
    object_type = models.ForeignKey(ContentType)
    generic_obj = generic.GenericForeignKey('object_type', 'object_id')

    account_type = models.ForeignKey('stores.LinkType', related_name='+')
    account_name = models.CharField('Account Name', max_length=200)

    @property
    def url(self):
        if self.account_type.url_format == '':
            return None
        return self.account_type.url_format % {'account': self.account_name}

    @property
    def to_html(self):
        dt = {
            'url': self.url,
            'name': self.account_name,
            'type_name': self.account_type,
            'type_icon': self.account_type.icon,
        }
        return render_to_string('stores/link_snippet.html', dt)

    def __unicode__(self):
        return u'%s - %s' % (self.account_type, self.account_name)

    class Meta:
        app_label = 'stores'