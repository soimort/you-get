#!/usr/bin/env python

import unittest

from you_get.extractors import (
    missevan
)


class YouGetTests(unittest.TestCase):
    def test_missevan(self):
        missevan.download('https://www.missevan.com/sound/player?id=2853120', info_only=True)


if __name__ == '__main__':
    unittest.main()
