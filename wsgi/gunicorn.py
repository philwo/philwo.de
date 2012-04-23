# -*- coding: utf-8 -*-

import os.path
#import multiprocessing

MY_PATH = os.path.abspath(os.path.split(__file__)[0])

bind = 'unix:%s' % (os.path.join(MY_PATH, 'gunicorn.sock'),)
workers = 2  # multiprocessing.cpu_count() * 2 + 1
user = 'philwo'
group = 'philwo'
umask = '0000'
pythonpath = os.path.abspath(os.path.join(MY_PATH, '..'))
