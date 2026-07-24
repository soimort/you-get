#!/usr/bin/env python

import unittest

from you_get.extractors import (
    imgur,
    magisto,
    youtube,
    missevan,
    acfun,
    bilibili,
    soundcloud,
    tiktok,
    twitter,
    miaopai,
    zhihu
)


class YouGetTests(unittest.TestCase):
    def test_imgur(self):
        imgur.download('http://imgur.com/WVLk5nD', info_only=True)
        imgur.download('https://imgur.com/we-should-have-listened-WVLk5nD', info_only=True)

    def test_magisto(self):
        magisto.download(
            'http://www.magisto.com/album/video/f3x9AAQORAkfDnIFDA',
            info_only=True
        )

    #def test_youtube(self):
        #youtube.download(
        #    'http://www.youtube.com/watch?v=pzKerr0JIPA', info_only=True
        #)
        #youtube.download('http://youtu.be/pzKerr0JIPA', info_only=True)
        #youtube.download(
        #    'http://www.youtube.com/attribution_link?u=/watch?v%3DldAKIzq7bvs%26feature%3Dshare',  # noqa
        #    info_only=True
        #)
        #youtube.download(
        #    'https://www.youtube.com/watch?v=oRdxUFDoQe0', info_only=True
        #)

    def test_acfun(self):
        acfun.download('https://www.acfun.cn/v/ac44560432', info_only=True)

    #def test_bilibili(self):
        #bilibili.download('https://www.bilibili.com/video/BV1sL4y177sC', info_only=True)

    #def test_soundcloud(self):
        ## single song
        #soundcloud.download(
        #    'https://soundcloud.com/keiny-pham/impure-bird', info_only=True
        #)
        ## playlist
        #soundcloud.download(
        #    'https://soundcloud.com/anthony-flieger/sets/cytus', info_only=True
        #)

    def test_tiktok(self):
        tiktok.download('https://www.tiktok.com/@zukky_48/video/7398162058153315605', info_only=True)
        tiktok.download('https://www.tiktok.com/@/video/7398162058153315605', info_only=True)
        tiktok.download('https://t.tiktok.com/i18n/share/video/7398162058153315605/', info_only=True)
        tiktok.download('https://vt.tiktok.com/ZSYKjKt6M/', info_only=True)

    def test_twitter(self):
        twitter.download('https://twitter.com/elonmusk/status/1530516552084234244', info_only=True)
        twitter.download('https://x.com/elonmusk/status/1530516552084234244', info_only=True)

    def test_weibo(self):
        miaopai.download('https://video.weibo.com/show?fid=1034:4825403706245135', info_only=True)

    def test_zhihu(self):
        # Zhihu answer page with video, e.g.:
        # https://www.zhihu.com/question/452201264/answer/1987873926903269203
        # Note: Zhihu requires cookies (z_c0) for access.
        # Without cookies, HTTP 403 is expected.
        # This test ensures the extractor handles None title gracefully
        # (TypeError: argument of type 'NoneType' is not iterable).
        try:
            zhihu.download(
                'https://www.zhihu.com/question/267782048/answer/490720324',
                info_only=True
            )
        except Exception as e:
            # 403 Forbidden is expected without cookies
            if '403' in str(e) or 'Forbidden' in str(e):
                import sys
                print('Skipped: Zhihu requires authentication cookies', file=sys.stderr)
                return
            raise

if __name__ == '__main__':
    unittest.main()
