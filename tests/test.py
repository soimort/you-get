#!/usr/bin/env python

import unittest

from you_get.extractors import (
    imgur,
    magisto,
    youtube,
    bilibili,
    toutiao,
)


class YouGetTests(unittest.TestCase):
    def test_bilibili(self):
        bilibili.download('https://www.bilibili.com/bangumi/play/ep259653/',info_only=True)#未加入cookie，但即使加入cookie效果也一样

if __name__ == '__main__':
    unittest.main()
