#!/usr/bin/env python

import unittest

from you_get.extractors import (
    iqiyi
)


class YouGetTests(unittest.TestCase):
    def test_iqiyi(self):
        iqiyi.download("https://www.iqiyi.com/v_19rrjbdi0s.html",output_dir='./',merge=True,caption=True)
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
