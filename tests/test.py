#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from you_get import *
from you_get.__main__ import url_to_module

def test_urls(urls):
    for url in urls:
        url_to_module(url).download(url, info_only = True)

class YouGetTests(unittest.TestCase):
    
    def test_blip(self):
        test_urls([
            "http://blip.tv/clojure/sam-aaron-programming-music-with-overtone-5970273",
        ])
        
    def test_googleplus(self):
        test_urls([
            "http://plus.google.com/102663035987142737445/posts/jJRu43KQFT5",
            "http://plus.google.com/+%E5%B9%B3%E7%94%B0%E6%A2%A8%E5%A5%88/posts/jJRu43KQFT5",
            "http://plus.google.com/+平田梨奈/posts/jJRu43KQFT5",
            "http://plus.google.com/photos/102663035987142737445/albums/5844078581209509505/5844078587839097874",
            "http://plus.google.com/photos/+%E5%B9%B3%E7%94%B0%E6%A2%A8%E5%A5%88/albums/5844078581209509505/5844078587839097874",
            "http://plus.google.com/photos/+平田梨奈/albums/5844078581209509505/5844078587839097874",
        ])
        
    def test_jpopsuki(self):
        test_urls([
            "http://jpopsuki.tv/video/Dragon-Ash---Run-to-the-Sun/8ad7aec604badd0b0798cd999b63ae17",
        ])
        
    def test_mixcloud(self):
        test_urls([
            "http://www.mixcloud.com/beatbopz/beat-bopz-disco-mix/",
            "http://www.mixcloud.com/beatbopz/tokyo-taste-vol4/",
            "http://www.mixcloud.com/DJVadim/north-america-are-you-ready/",
        ])
        
    def test_vid48(self):
        test_urls([
            "http://vid48.com/watch_video.php?v=KXUSG8169U41",
        ])
        
    def test_vimeo(self):
        test_urls([
            "http://vimeo.com/56810854",
        ])
        
    def test_xiami(self):
        test_urls([
            "http://www.xiami.com/song/1769835121",
        ])
        
    def test_youtube(self):
        test_urls([
            "http://www.youtube.com/watch?v=pzKerr0JIPA",
            "http://youtu.be/pzKerr0JIPA",
        ])
