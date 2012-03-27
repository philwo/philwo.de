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
from fabric.operations import run, local, sudo
from fabric.context_managers import prefix, cd, lcd
from fabric.utils import abort
from fabric.contrib.files import sed

from local_settings import DATABASES

# abspath() will ensure, that there is no trailing slash at the end of the path
LOCAL_PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

DB_NAME = 'philwo_blog'
DB_USERNAME = 'philwo_blog'
DB_PASSWORD = DATABASES['default']['PASSWORD']
USER_USERNAME = 'philwo'
USER_MAIL = 'philipp.wollermann@gmail.com'
SERVER_USERNAME = 'philwo'
SERVER_HOSTNAME = 'konata.philwo.de'
SERVER_PATH = '~/www/philwo.de/philwo'
SERVER_RSYNCURL = '%s@%s:%s' % (SERVER_USERNAME, SERVER_HOSTNAME, SERVER_PATH,)
MY_APPS = ['base', 'articles', 'photos']


# Environments
def dev():
    env.hosts = ['localhost']
    env.project_path = LOCAL_PROJECT_PATH


def prod():
    env.hosts = [SERVER_HOSTNAME]
    env.project_path = '/home/philwo/www/philwo.de/philwo/'


# Migrations
def migrate_initial():
    with lcd(LOCAL_PROJECT_PATH):
        with prefix("source deploy/bin/activate"):
            for app in MY_APPS:
                local("rm -f %s/migrations/????_*" % (app,))
                local("./manage.py schemamigration %s --initial" % (app,))


def migrate_auto():
    with lcd(LOCAL_PROJECT_PATH):
        with prefix("source deploy/bin/activate"):
            for app in MY_APPS:
                local("./manage.py schemamigration %s --auto || true" % (app,))


def migrate():
    with cd(env.project_path):
        with prefix("source deploy/bin/activate"):
            run("./manage.py syncdb || true")
            for app in MY_APPS:
                local("./manage.py migrate %s || true" % (app,))


def bootstrap():
    with cd(env.project_path):
        #make_venv()
        with prefix("source deploy/bin/activate"):
            setup_db()
            run("rm -rf static")
            run("mkdir static")
            run("./manage.py clean_pyc")
            run("./manage.py collectstatic -v0 --noinput")
            run("./manage.py syncdb --noinput")
            run("./manage.py createcachetable cache")
            run("./manage.py migrate")
            run("./manage.py createsuperuser --username=%s --email=%s" % (USER_USERNAME, USER_MAIL,))


# virtualenv management
def make_venv():
    with cd(env.project_path):
        virtualenv = os.path.join(env.project_path, 'deploy')
        run("virtualenv2 --clear --no-site-packages --distribute %s" % (virtualenv,))
        with prefix("source deploy/bin/activate"):
            run("pip-2.7 install --requirement requirements.txt")


def update_venv():
    with cd(env.project_path):
        with prefix("source deploy/bin/activate"):
            run("pip-2.7 install --requirement requirements.txt")


# Database management
def setup_db():
    with cd(env.project_path):
        run('psql -d template1 -c "DROP DATABASE IF EXISTS %s"' % (DB_NAME,))
        run('psql -d template1 -c "DROP ROLE IF EXISTS %s"' % (DB_USERNAME,))
        run('psql -d template1 -c "CREATE ROLE %s NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ENCRYPTED PASSWORD \'%s\'"' % (DB_USERNAME, DB_PASSWORD,))
        run('psql -d template1 -c "CREATE DATABASE %s WITH OWNER=%s"' % (DB_NAME, DB_USERNAME,))
        run('psql -d template1 -c "GRANT ALL ON DATABASE %s TO %s WITH GRANT OPTION"' % (DB_NAME, DB_USERNAME,))
        run('psql -d %s -c "GRANT ALL ON SCHEMA public TO %s WITH GRANT OPTION"' % (DB_NAME, DB_USERNAME,))
        run('psql -d %s -c "DROP EXTENSION IF EXISTS plpgsql"' % (DB_NAME,))


def backup_db():
    with cd(env.project_path):
        run("pg_dump -Fc -Z9 --serializable-deferrable %s > %s.pg" % (DB_NAME, DB_NAME,))


def restore_db():
    setup_db()
    with cd(env.project_path):
        run("pg_restore -U%s -O -x -d %s %s.pg" % (DB_USERNAME, DB_NAME, DB_NAME,))


# Deployment
def deploy():
    local("rsync -av -e ssh --delete --exclude '/deploy/**' --exclude '/static/**' --exclude '*.pyc' %s/ %s/" % (LOCAL_PROJECT_PATH, SERVER_RSYNCURL,))
    with cd(env.project_path):
        with prefix("source deploy/bin/activate"):
            run("./manage.py collectstatic -v0 --noinput")
    sudo("systemctl restart django-philwo.de.service")


# Data transfer between dev and prod
def download_media():
    with lcd(LOCAL_PROJECT_PATH):
        local('rsync -av -e ssh --delete %s/media/ media/' % (SERVER_RSYNCURL,))


def pull_db():
    local("for table in `psql %s -c'\dt' -A | grep ^public | cut -d'|' -f2`; do psql %s -c\"drop table if exists $table cascade\"; done" % (DB_NAME, DB_NAME,))
    local("ssh %s@%s pg_dump -U%s -Fc -Z9 %s | pg_restore -U%s -O -x -d %s" % (SERVER_USERNAME, SERVER_HOSTNAME, DB_USERNAME, DB_NAME, DB_USERNAME, DB_NAME,))


def push_db():
    if 'localhost' in env.hosts:
        abort('Running push_db on localhost would destroy your database.')
    run("for table in `psql -Upostgres %s -c'\dt' -A | grep ^public | cut -d'|' -f2`; do psql -Upostgres %s -c\"drop table if exists $table cascade\"; done" % (DB_NAME, DB_NAME,))
    local("pg_dump -U%s -Fc -Z9 %s | ssh %s@%s pg_restore -U%s -O -x -d %s" % (DB_USERNAME, DB_NAME, SERVER_USERNAME, SERVER_HOSTNAME, DB_USERNAME, DB_NAME,))


# Little helpers
def runserver():
    with lcd(LOCAL_PROJECT_PATH):
        with prefix("source deploy/bin/activate"):
            local("./manage.py runserver")


def grep(what):
    with lcd(LOCAL_PROJECT_PATH):
        local("fgrep -ir %s %s templates wsgi *.py | grep -v 'Binary file .* matches'" % (what, " ".join(MY_APPS)))


def new_secretkey():
    with cd(env.project_path):
        secretkey = ''.join(random.choice(string.letters + string.digits) for i in xrange(50))
        sed('local_settings.py', '^SECRET_KEY.*', 'SECRET_KEY = "%s"' % (secretkey,))
        run("rm settings.py.bak")
