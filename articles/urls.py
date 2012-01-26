# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from articles import views
from articles.feeds import TagFeed, LatestEntries, TagFeedAtom, LatestEntriesAtom

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page>\d+)/$', views.display_blog_page, name='articles_in_month_page'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.display_blog_page, name='articles_in_month'),
)

urlpatterns += patterns('',
    url(r'^$', views.display_blog_page, name='articles_archive'),
    url(r'^page/(?P<page>\d+)/$', views.display_blog_page, name='articles_archive_page'),

    url(r'^tag/(?P<tag>.*)/page/(?P<page>\d+)/$', views.display_blog_page, name='articles_display_tag_page'),
    url(r'^tag/(?P<tag>.*)/$', views.display_blog_page, name='articles_display_tag'),

    url(r'^author/(?P<username>.*)/page/(?P<page>\d+)/$', views.display_blog_page, name='articles_by_author_page'),
    url(r'^author/(?P<username>.*)/$', views.display_blog_page, name='articles_by_author'),

    url(r'^(?P<year>\d{4})/(?P<slug>.*)/$', views.display_article, name='articles_display_article'),

    # AJAX
    url(r'^ajax/tag/autocomplete/$', views.ajax_tag_autocomplete, name='articles_tag_autocomplete'),

    # RSS
    url(r'^feeds/latest\.rss$', LatestEntries(), name='articles_rss_feed_latest'),
    url(r'^feeds/latest/$', LatestEntries()),
    url(r'^feeds/tag/(?P<slug>[\w_-]+)\.rss$', TagFeed(), name='articles_rss_feed_tag'),
    url(r'^feeds/tag/(?P<slug>[\w_-]+)/$', TagFeed()),

    # Atom
    url(r'^feeds/atom/latest\.xml$', LatestEntriesAtom(), name='articles_atom_feed_latest'),
    url(r'^feeds/atom/tag/(?P<slug>[\w_-]+)\.xml$', TagFeedAtom(), name='articles_atom_feed_tag'),
)
