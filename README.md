This is the source code on which my personal website www.philwo.de runs.
It's not meant to be a finished product you can use out-of-the-box, even though I tried to make most things configurable and not hardcoded to my personal data.
However, if you'd like to see how a working, real-life Django-based personal website could be designed, it may suit you well and be a helpful repository for ideas and concepts.

## Theme

I'm not a designer, but I like great design - so I didn't try to create a template on my own, but instead bought a good one.
I chose the "Photography Pro" Wordpress theme from The Theme Foundry (http://thethemefoundry.com/photography/) and ported it to Django Templates.
Because it's commercially licensed, I can't supply their CSS stylesheets and image files - but as they are a small and friendly company, you might just want to buy it yourself, if you like it, and support them.

## Settings

After cloning the repository, you should create a local_settings.py file which contains the following directives:

```python
# -*- coding: utf-8 -*-

# Administrators
ADMINS = (
    ('Your Name', 'your.name@example.com'),
)
MANAGERS = ADMINS

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '...',
        'USER': '...',
        'PASSWORD': '...',
        'HOST': '',
        'PORT': '',
    }
}

# E-Mail Configuration (example for using Google Mail)
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your.name@gmail.com'
EMAIL_HOST_PASSWORD = '...'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'your.name@gmail.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
SEND_BROKEN_LINK_EMAILS = False

# Internationalization
TIME_ZONE = 'Asia/Tokyo'

# Disqus API
DISQUS_FORUM_SHORTNAME = '...'

# Flickr API
FLICKR_API_KEY = '...'
FLICKR_USER_ID = '...'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '...'
```

## Credits

I used the awesome django-articles app by codekoala as the base for my own blog app.
Check it out: https://bitbucket.org/codekoala/django-articles

Several other libraries were used - they are fully credited in the LICENSE file.

Have fun playing around with this project.
