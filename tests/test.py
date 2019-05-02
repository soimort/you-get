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

    def test_toutiao(self):
        toutiao.download('https://www.365yg.com/i6640053613567675662/#mid=1611922564114440', info_only=True)

    def test_bilibili(self):
        bilibili.download_playlist_by_url('https://www.bilibili.com/bangumi/play/ss26875')

if __name__ == '__main__':
    unittest.main()
