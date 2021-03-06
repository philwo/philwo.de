# -*- coding: utf-8 -*-

# Administrators
ADMINS = (
    ('My Name', 'my.email@example'),
)
MANAGERS = ADMINS

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'my_blog',
        'USER': 'my_blog',
        'PASSWORD': '1234',
        'HOST': '',
        'PORT': '',
    }
}

# E-Mail Configuration
DEFAULT_FROM_EMAIL = 'my.email@example'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
SEND_BROKEN_LINK_EMAILS = False

# Disqus API
DISQUS_FORUM_SHORTNAME = 'example'

# Flickr API
FLICKR_API_KEY = '123456789123456789123456789'
FLICKR_USER_ID = '12341234@X99'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'abcabcabc'
