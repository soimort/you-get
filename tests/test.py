#!/usr/bin/env python

import unittest

from you_get.extractors import (
    dailymotion
)


class YouGetTests(unittest.TestCase):
    def test_dailymotion(self):
        dailymotion.download('https://www.dailymotion.com/video/k5vkmYOVf9nq77yBkow', info_only=True)
    def test_dailymotion2(self):
        dailymotion.download('https://www.dailymotion.com/embed/video/k5vkmYOVf9nq77yBkow', info_only=True)

if __name__ == '__main__':
    unittest.main()
