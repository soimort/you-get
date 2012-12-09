#!/usr/bin/env python3

PROJ_METADATA = 'you-get.json'

import os, json, imp
here = os.path.abspath(os.path.dirname(__file__))
proj_info = json.loads(open(os.path.join(here, PROJ_METADATA)).read())
README = open(os.path.join(here, 'README.txt')).read()
CHANGELOG = open(os.path.join(here, 'CHANGELOG.txt')).read()
VERSION = imp.load_source('version', os.path.join(here, 'you_get/version.py')).__version__

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
    
    long_description = README + '\n\n' + CHANGELOG,
    
    packages = find_packages(),
    
    platforms = 'any',
    zip_safe = False,
    include_package_data = True,
    
    classifiers = proj_info['classifiers'],
    
    entry_points = {'console_scripts': proj_info['console_scripts']}
)
