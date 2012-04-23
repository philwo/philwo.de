# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', direct_to_template, {'template': 'home.html'}),
    url(r'^blog/', include('articles.urls')),
    url(r'^photos/', include('photos.urls')),
    url(r'^robots\.txt$', direct_to_template, {'template': 'robots.txt', 'mimetype': 'text/plain'}),
)

legacy_urls = (
    (r'^gallery/$', '/photos/'),
    (r'^gallery/(?P<path>.+)/', '/photos/gallery/%(path)s/'),
)

for urltuple in legacy_urls:
    oldurl, newurl = urltuple
    urlpatterns += patterns('', (oldurl, 'django.views.generic.simple.redirect_to', {'url': newurl}))

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
