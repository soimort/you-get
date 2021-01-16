#!/usr/bin/env python

import unittest

from you_get.extractors import (
    soundcloud
)


class YouGetTests(unittest.TestCase):
    def test_soundcloud(self):
        ## single song
        soundcloud.download(
            'https://soundcloud.com/angelo-cicero/action-iii', info_only=True
        )


if __name__ == '__main__':
    unittest.main()
