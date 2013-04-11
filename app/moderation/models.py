from django.utils.timezone import now
from django.conf import settings
from django.db import models
try:
    from django.contrib.auth import get_user_model
    USER_MODEL = get_user_model()
except ImportError:
    from django.contrib.auth.models import User as USER_MODEL
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


DEFAULT_FLAGGING_STATUS = (
    (1, 'Reported'),
    (2, 'Updated by Moderator'),
    (3, 'Deleted by Moderator'),
    (4, 'No Action'),
)
FLAGGING_STATUS = getattr(settings, 'FLAGGING_STATUS', DEFAULT_FLAGGING_STATUS)


class FlagType(models.Model):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class FlaggedObject(models.Model):
    object_id = models.PositiveIntegerField()
    object_type = models.ForeignKey(ContentType)
    generic_obj = generic.GenericForeignKey('object_type', 'object_id')

    flag_type = models.ForeignKey('moderation.FlagType', related_name='+')
    note = models.TextField()
    status = models.PositiveIntegerField(choices=FLAGGING_STATUS, default=1)
    user = models.ForeignKey(USER_MODEL, related_name='+', null=True, blank=True)

    created = models.DateTimeField('Created Date/Time', default=now)
    changed = models.DateTimeField('Changed Date/Time', default=now)

    def save(self, **kwargs):
        self.changed = now()
        return super(FlaggedObject, self).save(**kwargs)