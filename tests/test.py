#!/usr/bin/env python

import unittest

from you_get.extractors import (
    bilibili,
    miaopai
)


class YouGetTests(unittest.TestCase):
    def test_bilibili(self):
        bilibili.download(
            "https://www.bilibili.com/video/BV1xT4y1T7xA/", info_only=True
        )
    def test_weibo(self):
        miaopai.download('https://weibo.com/1748075785/K4VLHbVQB', info_only=True)

if __name__ == '__main__':
    unittest.main()
