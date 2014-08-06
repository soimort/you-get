#!/usr/bin/env python

import unittest

from you_get import *
from you_get.extractors import *
from you_get.common import *

class YouGetTests(unittest.TestCase):

    def test_freesound(self):
        freesound.download("http://www.freesound.org/people/Corsica_S/sounds/184419/", info_only=True)

    def test_magisto(self):
        magisto.download("http://www.magisto.com/album/video/f3x9AAQORAkfDnIFDA", info_only=True)

    def test_mixcloud(self):
        mixcloud.download("http://www.mixcloud.com/beatbopz/beat-bopz-disco-mix/", info_only=True)
        mixcloud.download("http://www.mixcloud.com/DJVadim/north-america-are-you-ready/", info_only=True)

    def test_vimeo(self):
        vimeo.download("http://vimeo.com/56810854", info_only=True)

    def test_youtube(self):
        youtube.download("http://www.youtube.com/watch?v=pzKerr0JIPA", info_only=True)
        youtube.download("http://youtu.be/pzKerr0JIPA", info_only=True)
        youtube.download("http://www.youtube.com/attribution_link?u=/watch?v%3DldAKIzq7bvs%26feature%3Dshare", info_only=True)
