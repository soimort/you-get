#!/usr/bin/env python

import unittest

from you_get.extractors import (
    youku,
)


class YouGetTests(unittest.TestCase):
    def test_youku(self):
        youku.download('https://v.youku.com/v_show/id_XNDAwMjkxNTU2NA==.html', info_only=True)
        youtube.download('https://v.youku.com/v_show/id_XNDAwMjkxMDM0MA==.html', info_only=True)
        youtube.download('https://v.youku.com/v_show/id_XNDAwMjkxMzcwNA==.html', info_only=True)

if __name__ == '__main__':
    unittest.main()
