#!/usr/bin/env python

import unittest

from you_get.extractors import (
    imgur,
    magisto,
    youtube,
    missevan,
    acfun,
    bilibili,
    soundcloud,
    tiktok
)


class YouGetTests(unittest.TestCase):

    def test_bilibili(self):
        bilibili.download('https://www.bilibili.com/video/BV1fr4y1K7aR', info_only=True)

    #def test_soundcloud(self):
        ## single song
        #soundcloud.download(
        #    'https://soundcloud.com/keiny-pham/impure-bird', info_only=True
        #)
        ## playlist
        #soundcloud.download(
        #    'https://soundcloud.com/anthony-flieger/sets/cytus', info_only=True
        #)

    #def tests_tiktok(self):
    #    tiktok.download('https://www.tiktok.com/@nmb48_official/video/6850796940293164290', info_only=True)
    #    tiktok.download('https://t.tiktok.com/i18n/share/video/6850796940293164290/', info_only=True)
    #    tiktok.download('https://vt.tiktok.com/UGJR4R/', info_only=True)


if __name__ == '__main__':
    unittest.main()
