# -*- coding: utf-8 -*-

import os, sys


#sys.path.append(BASE_DIR)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TYPE: mysql/postgresql/sqlite
# if choosing sqlite, only need to fill in dbtype and dbname
DATABASES = {
    'TYPE': 'sqlite',
    'NAME': 'gitolite',
    'USER': 'gitolite',
    'PASS': 'gitolite',
    'HOST': 'localhost',
    'PORT': '3306',
}

TEMPLATES = {
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
}

STATIC_URL = '/static/'

STATIC_ROOT = '/var/www/html/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

KEY_DIRS = os.path.join(BASE_DIR, 'keydir')
