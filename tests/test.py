#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from you_get import *
from you_get.__main__ import url_to_module

class YouGetTests(unittest.TestCase):
    
    def test_vimeo(self):
        for url in [
            "http://vimeo.com/56810854",
        ]:
            url_to_module(url).download(url, info_only = True)
    
    def test_googleplus(self):
        for url in [
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
        
    def test_jpopsuki(self):
        for url in [
            "http://jpopsuki.tv/video/Dragon-Ash---Run-to-the-Sun/8ad7aec604badd0b0798cd999b63ae17",
        ]:
            url_to_module(url).download(url, info_only = True)
    
    def test_douban(self):
        for url in [
            "http://site.douban.com/caofang/",
        ]:
            url_to_module(url).download(url, info_only = True)
    
    def test_xiami(self):
        for url in [
            "http://www.xiami.com/song/1769835121",
        ]:
            url_to_module(url).download(url, info_only = True)
