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
    def test_bilibil(self):
        bilibili.download_playlist(
            "https://www.bilibili.com/video/av755179663", playlist=True, info_only=False, output_dir="./tmp", merge=True
        )

if __name__ == '__main__':
    unittest.main()
