# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('photos.views',
    url(r'^$', 'galleries', name='photos_galleries'),
    url(r'^gallery/(?P<slug>[\w.-]+)/', 'gallery', name='photos_gallery'),
    url(r'^photo/(?P<id>[\w.-]+)/', 'photo', name='photos_photo')
)
