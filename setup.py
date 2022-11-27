#!/usr/bin/env python3

import importlib
import json
import os

from setuptools import find_packages, setup


PROJ_NAME = 'you-get'
PACKAGE_NAME = 'you_get'

PROJ_METADATA = '%s.json' % PROJ_NAME

here = os.path.abspath(os.path.dirname(__file__))
proj_info = json.loads(open(os.path.join(here, PROJ_METADATA), encoding='utf-8').read())
try:
    README = open(os.path.join(here, 'README.rst'), encoding='utf-8').read()
except Exception:
    README = ""
CHANGELOG = open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8').read()
VERSION = importlib.load_source('version', os.path.join(here, 'src/%s/version.py' % PACKAGE_NAME)).__version__


setup(
    name = proj_info['name'],
    version = VERSION,

    author = proj_info['author'],
    author_email = proj_info['author_email'],
    url = proj_info['url'],
    license = proj_info['license'],

    description = proj_info['description'],
    keywords = proj_info['keywords'],

    long_description = README,

    packages = find_packages('src'),
    package_dir = {'' : 'src'},

    test_suite = 'tests',

    platforms = 'any',
    zip_safe = True,
    include_package_data = True,

    classifiers = proj_info['classifiers'],

    entry_points = {'console_scripts': proj_info['console_scripts']},

    extras_require={
        'socks': ['PySocks'],
    }
)
