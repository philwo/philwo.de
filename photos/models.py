# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class Photo(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    secret = models.CharField(max_length=100)
    server = models.CharField(max_length=100)
    farm = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)
    originalsecret = models.CharField(max_length=100, blank=True)
    originalformat = models.CharField(max_length=100, blank=True)
    o_width = models.IntegerField(null=True)
    o_height = models.IntegerField(null=True)
    date_taken = models.DateTimeField()

    class Meta:
        ordering = ['date_taken']

    def __unicode__(self):
        return u'%s' % (self.title,)

    @models.permalink
    def get_absolute_url(self):
        return ('photos.views.photo', (), {'id': self.id})

    def get_flickr_original_url(self):
        return 'http://farm%s.static.flickr.com/%s/%s_%s_o.%s' % (self.farm, self.server, self.id, self.originalsecret, self.originalformat)

    def get_flickr_square_url(self):
        return 'http://farm%s.static.flickr.com/%s/%s_%s_s.jpg' % (self.farm, self.server, self.id, self.secret)

    def get_flickr_thumbnail_url(self):
        return 'http://farm%s.static.flickr.com/%s/%s_%s_t.jpg' % (self.farm, self.server, self.id, self.secret)

    def get_flickr_small_url(self):
        return 'http://farm%s.static.flickr.com/%s/%s_%s_m.jpg' % (self.farm, self.server, self.id, self.secret)

    def get_flickr_medium500_url(self):
        return 'http://farm%s.static.flickr.com/%s/%s_%s.jpg' % (self.farm, self.server, self.id, self.secret)

    def get_flickr_medium640_url(self):
        return 'http://farm%s.static.flickr.com/%s/%s_%s_z.jpg' % (self.farm, self.server, self.id, self.secret)

    def get_flickr_large_url(self):
        return 'http://farm%s.static.flickr.com/%s/%s_%s_b.jpg' % (self.farm, self.server, self.id, self.secret)

    def get_link_to_flickr(self, set_id):
        return 'http://www.flickr.com/photos/philwo/%s/in/set-%s/' % (self.id, set_id)

    def get_gallery_url(self):
        return '%sphotos/gallery/%s.jpg' % (settings.MEDIA_URL, self.id,)

    def get_thumbnail_url(self):
        return '%sphotos/thumbnails/%s.jpg' % (settings.MEDIA_URL, self.id,)


class Photoset(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    primary = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)
    server = models.CharField(max_length=100)
    farm = models.CharField(max_length=100)
    photo_count = models.IntegerField()
    title = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photos = models.ManyToManyField(Photo)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'%s' % (self.title,)

    @models.permalink
    def get_absolute_url(self):
        return ('photos.views.gallery', (), {'slug': self.slug})

    def get_primary(self):
        return Photo.objects.get(pk=self.primary)
