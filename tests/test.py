#!/usr/bin/env python

import unittest

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
        bilibili.download(
            'https://www.bilibili.com/video/av16907446/', info_only=True
        )
        bilibili.download(
            'https://www.bilibili.com/video/av13228063/', info_only=True
        )

    def test_sohu(self):
        sohu_download.download(
            'https://tv.sohu.com/v/cGwvOTQ0Nzk1Ni8xMDIxMTMwMjguc2h0bWw=.html', info_only=True
        )
        sohu_download.download(
            'https://tv.sohu.com/v/cGwvOTI5ODkyOC85OTk0ODY5Mi5zaHRtbA==.html', info_only=True
        )


if __name__ == '__main__':
    unittest.main()
