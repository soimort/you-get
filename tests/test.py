#!/usr/bin/env python

import os
import unittest
from tempfile import TemporaryDirectory

import you_get.common
from you_get.extractors import (
    imgur,
    magisto,
    youtube,
    missevan,
    acfun,
    bilibili
)


class YouGetTests(unittest.TestCase):
    def test_imgur(self):
        imgur.download('http://imgur.com/WVLk5nD', info_only=True)

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
        youtube.download(
            'https://www.youtube.com/watch?v=Fpr4fQSh1cc', info_only=True
        )

    def test_acfun(self):
        acfun.download('https://www.acfun.cn/v/ac11701912', info_only=True)

    def test_bilibil(self):
        bilibili.download(
            "https://www.bilibili.com/watchlater/#/BV1PE411q7mZ/p6", info_only=True
        )
        bilibili.download(
            "https://www.bilibili.com/watchlater/#/av74906671/p6", info_only=True
        )
        with TemporaryDirectory() as temp_dir:
            output_filename_bak = you_get.common.output_filename
            try:
                you_get.common.output_filename = 'cat'  # Simulate argument "--output-filename cat"
                bilibili.download(
                    'https://www.bilibili.com/video/BV1jJ411x724',  # A very short video
                    output_dir=temp_dir,
                    merge=True,
                    caption=True,  # We want danmaku file
                )
                self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'cat.mp4')))
                self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'cat.cmt.xml')))
            finally:
                you_get.common.output_filename = output_filename_bak  # Restore side-effect


if __name__ == '__main__':
    unittest.main()
