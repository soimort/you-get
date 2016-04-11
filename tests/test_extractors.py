#!/usr/bin/env python

import unittest

from you_get.extractors import *

class YouTubeTests(unittest.TestCase):

    def test_download(self):
        youtube.download("http://www.youtube.com/watch?v=pzKerr0JIPA", info_only=True)
        youtube.download("http://youtu.be/pzKerr0JIPA", info_only=True)
        youtube.download("http://www.youtube.com/attribution_link?u=/watch?v%3DldAKIzq7bvs%26feature%3Dshare", info_only=True)

    def test_download_playlist(self):
        youtube.download_playlist("https://www.youtube.com/playlist?list=PLgjdyCiEceFiXM8veBtbOOMfyeWsoMinG", info_only=True)

    def test_get_url_from_vid(self):
        self.assertEqual(YouTube.get_url_from_vid('tdsTfZMqAxw'), 'https://youtu.be/tdsTfZMqAxw')

    def test_get_vid_from_url(self):
        self.assertEqual(YouTube.get_vid_from_url('https://www.youtube.com/watch?v=c3BlRCGPEbs'),
                         'c3BlRCGPEbs')

    def test_get_playlist_id_from_url(self):
        self.assertEqual(YouTube.get_playlist_id_from_url('https://www.youtube.com/watch?v=VbfpW0pbvaU&index=10&list=PLDcnymzs18LVXfO_x0Ei0R24qDbVtyy66'),
                         'PLDcnymzs18LVXfO_x0Ei0R24qDbVtyy66')


class XiamiTests(unittest.TestCase):

    def test_download_video(self):
        xiami.download("http://www.xiami.com/play?ids=/song/playlist/id/1/type/9#open", info_only=True)

    def test_download_pic(self):
        xiami.download("http://www.xiami.com/artist/pic-detail/pid/13452?spm=0.0.0.0.2lEgvQ", info_only=True)

    def test_download_song(self):
        xiami.download("http://www.xiami.com/song/1775852230?spm=a1z1s.7400859.1392350021.4.oSFNmx", info_only=True)

    def test_download_album(self):
        xiami.download("http://www.xiami.com/album/2100217288?spm=a1z1s.7400860.1392350021.1.m0BAKq", info_only=True)


class InstagramTests(unittest.TestCase):

    def test_download_video(self):
        instagram.download("https://www.instagram.com/p/BD8w6M3Pxei/", info_only=True)

    def test_download_image(self):
        instagram.download("https://www.instagram.com/p/BD8lTLIvxTn/", info_only=True)


class TwitterTests(unittest.TestCase):

    def test_download_video(self):
        twitter.download("https://twitter.com/BlueJays/status/719272038318284800?lang=en", info_only=True)

    def test_download_image(self):
        twitter.download("https://twitter.com/Raptors/status/719350726745567232", info_only=True)


class VineTests(unittest.TestCase):

    def test_download_video(self):
        vine.download("https://vine.co/v/MDl3QL0rK50", info_only=True)

    def test_download_card(self):
        vine.download("https://vine.co/v/iITOeY0mDuZ", info_only=True)


class SoundcloudTests(unittest.TestCase):

    def test_download_song(self):
        soundcloud.download("https://soundcloud.com/nettwerkmusicgroup/angus-julia-stone-the-devils-tears", info_only=True)


class PinterestTests(unittest.TestCase):

    def test_download(self):
        pinterest.download("https://www.pinterest.com/pin/177962622746499307/", info_only=True)


class VimeoTests(unittest.TestCase):

    def test_download(self):
        vimeo.download("http://vimeo.com/56810854", info_only=True)


class TumblrTests(unittest.TestCase):

    def test_download(self):
        tumblr.download("http://ben-smith-123.tumblr.com/post/138801913226", info_only=True)


class TedTests(unittest.TestCase):

    def test_download(self):
        ted.download("https://www.ted.com/talks/linus_torvalds_the_mind_behind_linux", info_only=True)

