# -*- coding: utf-8 -*-

import os
import os.path

PROJECT_PATH = os.path.abspath(os.path.join(os.path.split(__file__)[0], '..'))

# Debugging
DEBUG = False
TEMPLATE_DEBUG = DEBUG
if TEMPLATE_DEBUG:
    TEMPLATE_STRING_IF_INVALID = 'TEMPLATE_INVALID'
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

# Administrators
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                       # Or path to database file if using sqlite3.
        'USER': '',                       # Not used with sqlite3.
        'PASSWORD': '',                   # Not used with sqlite3.
        'HOST': '',                       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                       # Set to empty string for default. Not used with sqlite3.
    }
}

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}

# URL Canonicalization and Configuration
APPEND_SLASH = True
PREPEND_WWW = False
ROOT_URLCONF = 'philwo.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'philwo.wsgi.application'

# Multiple Sites Handling
SITE_ID = 1

# Internationalization
_ = lambda s: s
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en', _('English'))
)
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'Asia/Tokyo'
USE_TZ = True

# Session Handling
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Disqus API
DISQUS_FORUM_SHORTNAME = ''

# Flickr API
FLICKR_API_KEY = ''
FLICKR_USER_ID = ''

# Automatic generation of article slugs
from django.template.defaultfilters import slugify
AUTOSLUG_SLUGIFY_FUNCTION = lambda s: slugify(s.lower().replace(u"ä", u"ae").replace(u"ü", u"ue").replace(u"ö", u"oe"))

# Uploads
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

# Static files
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# Increase Cookie Security
if not DEBUG:
    SESSION_COOKIE_SECURE = True

# Security - Prevent Clickjacking
X_FRAME_OPTIONS = 'DENY'

# HTTP Optimization
USE_ETAGS = True

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'base.middleware.RemoveEmptyLinesMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

# Static Files
STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Template - Context Processors
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "base.context_processors.access_settings",
    "base.context_processors.useragent",
    "base.context_processors.DjangoVersionContextProcessor",
    "base.context_processors.PythonVersionContextProcessor",
)

# Template - Loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

# Template - Directories
TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
    os.path.join(PROJECT_PATH, 'base', "templates"),
    os.path.join(PROJECT_PATH, 'articles', "templates"),
)

# Applications
OUR_APPS = (
    'base',
    'articles',
    'photos',
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.flatpages',
    'django_extensions',
    'typogrify',
    'tagging',
    'south',
    'gunicorn',
    'devserver',
) + OUR_APPS

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from local_settings import *
except ImportError:
    pass
