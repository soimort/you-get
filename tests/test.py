#!/usr/bin/env python

import unittest

from you_get.extractors import (
    bilibili,
)


class YouGetTests(unittest.TestCase):	
    def test_bilibili(self):

        bilibili.download('https://space.bilibili.com/19111402/video', info_only=True)
        youtube.download('https://space.bilibili.com/19111402/video', info_only=True)

if __name__ == '__main__':
    unittest.main()
