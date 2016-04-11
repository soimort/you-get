#!/usr/bin/env python

import unittest

from you_get import *
from you_get.extractors import *
from you_get.common import *

class YouGetTests(unittest.TestCase):

    def test_freesound(self):
        freesound.download("http://www.freesound.org/people/Corsica_S/sounds/184419/", info_only=True)

    def test_imgur(self):
        imgur.download("http://imgur.com/WVLk5nD", info_only=True)
        imgur.download("http://imgur.com/gallery/WVLk5nD", info_only=True)

    def test_magisto(self):
        magisto.download("http://www.magisto.com/album/video/f3x9AAQORAkfDnIFDA", info_only=True)

    def test_mixcloud(self):
        mixcloud.download("http://www.mixcloud.com/DJVadim/north-america-are-you-ready/", info_only=True)
