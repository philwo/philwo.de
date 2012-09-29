# -*- coding: utf-8 -*-

DEBUG = True

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
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.example.com'
EMAIL_HOST_USER = 'my.email@example'
EMAIL_HOST_PASSWORD = '1234'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'my.email@example'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
SEND_BROKEN_LINK_EMAILS = False

# Internationalization
TIME_ZONE = 'Asia/Tokyo'

# Disqus API
DISQUS_FORUM_SHORTNAME = 'philwo'

# Flickr API
FLICKR_API_KEY = '123456789123456789123456789'
FLICKR_USER_ID = '12341234@X99'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'abcabcabc'
