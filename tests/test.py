#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from you_get import *
from you_get.__main__ import url_to_module

class YouGetTests(unittest.TestCase):
    
    def test_googleplus(self):
        for url in [ 
            "http://plus.google.com/111438309227794971277/posts/So6bW37WWtp",
            "http://plus.google.com/114038303885145553998/posts/7Jkwa35HZu8",
            "http://plus.google.com/109544372058574620997/posts/Hn9P3Mbuyud",
            "http://plus.google.com/photos/109544372058574620997/albums/5835145047890484737/5835145057636064194",
            "http://plus.google.com/102663035987142737445/posts/jJRu43KQFT5",
            "http://plus.google.com/+%E5%B9%B3%E7%94%B0%E6%A2%A8%E5%A5%88/posts/jJRu43KQFT5",
            "http://plus.google.com/+平田梨奈/posts/jJRu43KQFT5",
            "http://plus.google.com/photos/102663035987142737445/albums/5844078581209509505/5844078587839097874",
            "http://plus.google.com/photos/+%E5%B9%B3%E7%94%B0%E6%A2%A8%E5%A5%88/albums/5844078581209509505/5844078587839097874",
            "http://plus.google.com/photos/+平田梨奈/albums/5844078581209509505/5844078587839097874",
        ]:
            url_to_module(url).download(url, info_only = True)
        
    def test_mixcloud(self):
        for url in [ 
            "http://www.mixcloud.com/beatbopz/beat-bopz-disco-mix/",
            "http://www.mixcloud.com/beatbopz/tokyo-taste-vol4/",
            "http://www.mixcloud.com/DJVadim/north-america-are-you-ready/",
        ]:
            url_to_module(url).download(url, info_only = True)
