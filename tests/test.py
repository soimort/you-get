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
    def test_youtube(self):
        youtube.download(
            'https://www.youtube.com/watch?v=yS2rcvR6tFI', info_only=True
        )


if __name__ == '__main__':
    unittest.main()
