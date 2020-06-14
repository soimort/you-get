#!/usr/bin/env python

import unittest

from you_get.extractors import (
    imgur,
    magisto,
    youtube,
    missevan,
    acfun,
    bilibili,
    baidu
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

    def test_baidu_haokan(self):
        baidu.download(
            'https://haokan.baidu.com/v?vid=6794443542184039159&pd=bjh&fr=bjhauthor&type=video', info_only=True
        )

if __name__ == '__main__':
    unittest.main()
