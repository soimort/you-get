#!/usr/bin/env python3

PROJ_METADATA = 'you-get.json'

import os, json

here = os.path.abspath(os.path.dirname(__file__))
proj_info = json.loads(open(os.path.join(here, PROJ_METADATA)).read())
README = open(os.path.join(here, 'README.txt')).read()
CHANGELOG = open(os.path.join(here, 'CHANGELOG.txt')).read()

from distutils.core import setup
setup(
    name = proj_info['name'],
    version = proj_info['version'],
    
    author = proj_info['author'],
    author_email = proj_info['author_email'],
    url = proj_info['url'],
    download_url = proj_info['download_url'],
    license = proj_info['license'],
    
    description = proj_info['description'],
    keywords = proj_info['keywords'],
    long_description = README + '\n\n' + CHANGELOG,
    
    packages = proj_info['packages'],
    
    classifiers = proj_info['classifiers']
)
