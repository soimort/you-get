#!/usr/bin/env python

import unittest

from you_get.extractors import (
    bilibili,
)


class YouGetTests(unittest.TestCase):
        def test_bilibili(self):
            bilibili.download('https://www.bilibili.com/video/av8977143', info_only=True)

if __name__ == '__main__':
    unittest.main()
