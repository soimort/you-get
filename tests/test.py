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
    def test_imgur(self):
        imgur.download('http://imgur.com/WVLk5nD', info_only=True)

    def test_magisto(self):
        magisto.download(
            'http://www.magisto.com/album/video/f3x9AAQORAkfDnIFDA',
            info_only=True
        )

    def test_youtube(self):
        youtube.download(
            'http://www.youtube.com/watch?v=pzKerr0JIPA', info_only=True
        )
        youtube.download('http://youtu.be/pzKerr0JIPA', info_only=True)
        youtube.download(
            'http://www.youtube.com/attribution_link?u=/watch?v%3DldAKIzq7bvs%26feature%3Dshare',  # noqa
            info_only=True
        )
        #youtube.download(
        #    'https://www.youtube.com/watch?v=Fpr4fQSh1cc', info_only=True
        #)

    def test_acfun(self):
        acfun.download('https://www.acfun.cn/v/ac11701912', info_only=True)

    def test_bilibili(self):
        bilibili.download(
            "https://www.bilibili.com/watchlater/#/BV1PE411q7mZ/p6", info_only=True
        )
        bilibili.download(
            "https://www.bilibili.com/watchlater/#/av74906671/p6", info_only=True
        )

    def test_soundcloud(self):
        ## single song
        soundcloud.download(
            'https://soundcloud.com/keiny-pham/impure-bird', info_only=True
        )
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
