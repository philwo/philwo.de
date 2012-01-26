# -*- coding: utf-8 -*-

import sys
import django
from django.conf import settings
from django.contrib.sites.models import Site


def access_settings(request):
    data = {}
    data["DEBUG"] = getattr(settings, 'DEBUG', False)
    data["DISQUS_FORUM_SHORTNAME"] = getattr(settings, 'DISQUS_FORUM_SHORTNAME', None)
    data["current_site"] = Site.objects.get_current()
    return data


def useragent(request):
    data = {}
    if "HTTP_USER_AGENT" in request.META:
        useragent = request.META["HTTP_USER_AGENT"]
        data["is_ie6"] = "MSIE 6.0" in useragent
    return data


def DjangoVersionContextProcessor(request):
    one, two, three, four, five = django.VERSION
    return {'DJANGO_VERSION': '%s.%s.%s' % (one, two, three)}


def PythonVersionContextProcessor(request):
    one, two, three, four, five = sys.version_info
    return {'PYTHON_VERSION': '%s.%s.%s' % (one, two, three)}
