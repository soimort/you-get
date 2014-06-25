#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from you_get import *
from you_get.extractor.__main__ import url_to_module

def test_urls(urls):
    for url in urls:
        url_to_module(url)[0].download(url, info_only = True)

class YouGetTests(unittest.TestCase):

    def test_freesound(self):
        test_urls([
            "http://www.freesound.org/people/Corsica_S/sounds/184419/",
        ])

    def test_magisto(self):
        test_urls([
            "http://www.magisto.com/album/video/f3x9AAQORAkfDnIFDA",
        ])

    def test_mixcloud(self):
        test_urls([
            "http://www.mixcloud.com/beatbopz/beat-bopz-disco-mix/",
            "http://www.mixcloud.com/DJVadim/north-america-are-you-ready/",
        ])

    def test_ted(self):
        test_urls([
            "http://www.ted.com/talks/jennifer_lin_improvs_piano_magic.html",
            "http://www.ted.com/talks/derek_paravicini_and_adam_ockelford_in_the_key_of_genius.html",
        ])

    def test_vimeo(self):
        test_urls([
            "http://vimeo.com/56810854",
        ])

    def test_youtube(self):
        test_urls([
            "http://www.youtube.com/watch?v=pzKerr0JIPA",
            "http://youtu.be/pzKerr0JIPA",
            "http://www.youtube.com/attribution_link?u=/watch?v%3DldAKIzq7bvs%26feature%3Dshare"
        ])
