# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from base.storages import OverwriteImageStorage


def avatar_filename(instance, filename):
    return "uploads/avatars/%s" % (instance.user.username,)


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=True)
    avatar = models.ImageField(upload_to=avatar_filename, storage=OverwriteImageStorage(), width_field="avatar_width", height_field="avatar_height", blank=True)
    avatar_width = models.IntegerField(editable=False, default=0)
    avatar_height = models.IntegerField(editable=False, default=0)

    def __unicode__(self):
        return u"<UserProfile #%s: %s>" % (self.id, self.user)


def user_post_save(sender, instance, **kwargs):
    """
    Automatically create a user profile, when a user gets created.
    """
    profile, new = UserProfile.objects.get_or_create(user=instance)
models.signals.post_save.connect(user_post_save, sender=User)
