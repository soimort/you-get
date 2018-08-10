#!/usr/bin/env python

import unittest
import urllib

from you_get.extractors import (
    imgur,
    magisto,
    youtube,
    bilibili,
)


class YouGetTests(unittest.TestCase):
    def test_imgur(self):
        imgur.download('http://imgur.com/WVLk5nD', info_only=True)
        imgur.download('http://imgur.com/gallery/WVLk5nD', info_only=True)

    def test_magisto(self):
        magisto.download(
            'http://www.magisto.com/album/video/f3x9AAQORAkfDnIFDA',
            info_only=True
        )

    def test_youtube(self):
        youtube.download(
            'http://www.youtube.com/watch?v=pzKerr0JIPA', info_only=True
        )
        youtube.download('http://youtu.be/pzKerr0JIPA', info_only=True)
        youtube.download(
            'http://www.youtube.com/attribution_link?u=/watch?v%3DldAKIzq7bvs%26feature%3Dshare',  # noqa
            info_only=True
        )

    def test_bilibili(self):
        maxRetry = 3

        # the bilibi is not stable, it got 502 occasionally
        for i in range(maxRetry):
            try:
                bilibili.download(
                    'https://www.bilibili.com/video/av16907446/', info_only=True
                )
                bilibili.download(
                    'https://www.bilibili.com/video/av13228063/', info_only=True
                )
                return
            except urllib.error.HTTPError as e:
                if e.error == 502 and i + 1 < maxRetry:
                    continue
                else:
                    raise e


if __name__ == '__main__':
    unittest.main()
