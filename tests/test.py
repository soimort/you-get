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
        bilibili.download("https://live.bilibili.com/record/R1qx411c7hJ", info_only=True)


if __name__ == '__main__':
    unittest.main()
