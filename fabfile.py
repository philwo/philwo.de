#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import os.path
import random
import string

# available fabric.* functions are listed here:
# https://github.com/fabric/fabric/blob/master/fabric/api.py
from fabric.state import env
from fabric.operations import run, local
from fabric.context_managers import prefix, cd, lcd
#from fabric.utils import abort
from fabric.contrib.files import sed

from local_settings import DATABASES

# abspath() will ensure, that there is no trailing slash at the end of the path
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

DB_NAME = 'philwo_blog'
DB_USERNAME = 'philwo_blog'
DB_PASSWORD = DATABASES['default']['PASSWORD']
USER_USERNAME = 'philwo'
USER_MAIL = 'philipp.wollermann@gmail.com'
SERVER_USERNAME = 'philwo'
SERVER_HOSTNAME = 'rory.philwo.de'
SERVER_PATH = '~/www/philwo.de/philwo'
SERVER_RSYNCURL = '%s@%s:%s' % (SERVER_USERNAME, SERVER_HOSTNAME, SERVER_PATH,)

env.hosts = [SERVER_HOSTNAME]


def runserver():
    with lcd(PROJECT_PATH):
        with prefix("source deploy/bin/activate"):
            local("./manage.py runserver")


def migrate_initial():
    with lcd(PROJECT_PATH):
        with prefix("source deploy/bin/activate"):
            local("rm -f base/migrations/????_*")
            local("rm -f articles/migrations/????_*")
            local("rm -f photos/migrations/????_*")
            local("./manage.py schemamigration base --initial")
            local("./manage.py schemamigration articles --initial")
            local("./manage.py schemamigration photos --initial")


def migrate_auto():
    with lcd(PROJECT_PATH):
        with prefix("source deploy/bin/activate"):
            local("./manage.py schemamigration base --auto || true")
            local("./manage.py schemamigration articles --auto || true")
            local("./manage.py schemamigration photos --auto || true")


def reset():
    with lcd(PROJECT_PATH):
        with prefix("source deploy/bin/activate"):
            local("psql -d template1 -c \"DROP DATABASE IF EXISTS %s;\"" % (DB_NAME,))
            local("psql -d template1 -c \"DROP ROLE IF EXISTS %s;\"" % (DB_USERNAME,))
            local("psql -d template1 -c \"CREATE ROLE %s NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ENCRYPTED PASSWORD '%s';\"" % (DB_USERNAME, DB_PASSWORD,))
            local("psql -d template1 -c \"CREATE DATABASE %s WITH OWNER=%s;\"" % (DB_NAME, DB_USERNAME,))
            local("psql -d %s -c \"GRANT ALL ON SCHEMA public TO %s WITH GRANT OPTION;\"" % (DB_NAME, DB_USERNAME,))
            local("rm -rf static")
            local("mkdir static")
            local("./manage.py clean_pyc")
            local("./manage.py syncdb --noinput")
            local("./manage.py createcachetable cache")
            local("./manage.py migrate")
            local("./manage.py createsuperuser --username=%s --email=%s" % (USER_USERNAME, USER_MAIL,))
            local("./manage.py collectstatic -v0 --noinput")


def make_venv():
    with cd(PROJECT_PATH):
        #if "VIRTUAL_ENV" not in os.environ:
        #    abort("$VIRTUAL_ENV not found.\n\n")
        #virtualenv = os.environ["VIRTUAL_ENV"]
        virtualenv = os.path.join(PROJECT_PATH, 'deploy')
        run("virtualenv2 --clear --no-site-packages --distribute %s" % (virtualenv,))
        run("pip-2.7 install -E %s --requirement requirements.txt" % (virtualenv,))


def update_venv():
    with cd(PROJECT_PATH):
        #if "VIRTUAL_ENV" not in os.environ:
        #    abort("$VIRTUAL_ENV not found.\n\n")
        #virtualenv = os.environ["VIRTUAL_ENV"]
        virtualenv = os.path.join(PROJECT_PATH, 'deploy')
        run("pip-2.7 install -E %s --requirement requirements.txt" % (virtualenv,))


def new_secretkey():
    with cd(PROJECT_PATH):
        secretkey = ''.join(random.choice(string.letters + string.digits) for i in xrange(50))
        sed('settings.py', '^SECRET_KEY.*', 'SECRET_KEY = "%s"' % (secretkey,))
        run("rm settings.py.bak")


def download_media():
    with cd(PROJECT_PATH):
        run('rsync -av -e ssh --delete %s/media/ media/' % (SERVER_RSYNCURL,))


def deploy():
    run("rsync -av -e ssh --delete --exclude 'deploy/**' --exclude 'static/**' --exclude '*.pyc' %s/ %s/" % (PROJECT_PATH, SERVER_RSYNCURL,))


def backup_db():
    with cd(PROJECT_PATH):
        run("pg_dump -Fc -Z9 --serializable-deferrable %s > %s.pg" % (DB_NAME, DB_NAME,))


def restore_db():
    with cd(PROJECT_PATH):
        run("psql -d template1 -c \"DROP DATABASE IF EXISTS %s;\"" % (DB_NAME,))
        run("psql -d template1 -c \"DROP ROLE IF EXISTS %s;\"" % (DB_USERNAME,))
        run("psql -d template1 -c \"CREATE ROLE %s NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ENCRYPTED PASSWORD '%s';\"" % (DB_USERNAME, DB_PASSWORD,))
        run("psql -d template1 -c \"CREATE DATABASE %s WITH OWNER=%s;\"" % (DB_NAME, DB_USERNAME,))
        run("pg_restore -O -d %s %s.pg" % (DB_NAME, DB_NAME,))


def pull_db():
    local("ssh %s@%s pg_dump -Fc -Z9 --serializable-deferrable | pg_restore -O -d %s" % (SERVER_USERNAME, SERVER_HOSTNAME, DB_NAME,))


def push_db():
    local("pg_dump -Fc -Z9 --serializable-deferrable | ssh %s@%s pg_restore -O -d %s" % (SERVER_USERNAME, SERVER_HOSTNAME, DB_NAME,))


def grep(what):
    with cd(PROJECT_PATH):
        local("fgrep -ir %s articles base photos templates wsgi *.py | grep -v 'Binary file .* matches'" % (what,))
