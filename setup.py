#!/usr/bin/env python3

PROJ_NAME = 'you-get'
PACKAGE_NAME = 'you_get'

PROJ_METADATA = '%s.json' % PROJ_NAME

import importlib.util
import importlib.machinery

def load_source(modname, filename):
    loader = importlib.machinery.SourceFileLoader(modname, filename)
    spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
    module = importlib.util.module_from_spec(spec)
    # The module is always executed and not cached in sys.modules.
    # Uncomment the following line to cache the module.
    # sys.modules[module.__name__] = module
    loader.exec_module(module)
    return module

import os, json
here = os.path.abspath(os.path.dirname(__file__))
proj_info = json.loads(open(os.path.join(here, PROJ_METADATA), encoding='utf-8').read())
try:
    README = open(os.path.join(here, 'README.rst'), encoding='utf-8').read()
except:
    README = ""
CHANGELOG = open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf-8').read()
VERSION = load_source('version', os.path.join(here, 'src/%s/version.py' % PACKAGE_NAME)).__version__

from setuptools import setup, find_packages
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

    install_requires = ['dukpy'],
    extras_require = {
        'socks': ['PySocks'],
    }
)
