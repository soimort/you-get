#!/usr/bin/env python

import copy
import json
import unittest
from unittest.mock import patch

from you_get.extractors import bilibili


class TestBilibili(unittest.TestCase):
    video_url = 'https://www.bilibili.com/video/BV1TestVideo/'

    @staticmethod
    def video_info(pages=None):
        pages = pages or [
            {'cid': 456, 'page': 1, 'part': 'Part 1', 'duration': 60},
        ]
        return {
            'aid': 123,
            'bvid': 'BV1TestVideo',
            'title': 'API metadata title',
            'videos': len(pages),
            'pages': pages,
        }

    @staticmethod
    def playinfo():
        return {
            'code': 0,
            'message': '0',
            'data': {
                'quality': 112,
                'accept_quality': [112, 80, 64, 32, 16],
                'dash': {
                    'video': [
                        {
                            'id': 112,
                            'codecid': 7,
                            'codecs': 'avc1.640032',
                            'baseUrl': 'https://cdn.example/video-112.m4s',
                        },
                        {
                            'id': 16,
                            'codecid': 7,
                            'codecs': 'avc1.64001e',
                            'baseUrl': 'https://cdn.example/video-16.m4s',
                        },
                    ],
                    'audio': [
                        {
                            'id': 30216,
                            'bandwidth': 66147,
                            'codecs': 'mp4a.40.2',
                            'baseUrl': 'https://cdn.example/audio-30216.m4s',
                        },
                        {
                            'id': 30280,
                            'bandwidth': 200388,
                            'codecs': 'mp4a.40.2',
                            'baseUrl': 'https://cdn.example/audio-30280.m4s',
                        },
                        {
                            'id': 30232,
                            'bandwidth': 116896,
                            'codecs': 'mp4a.40.2',
                            'baseUrl': 'https://cdn.example/audio-30232.m4s',
                        },
                    ],
                },
            },
        }

    def make_get_content(self, video_info=None):
        video_info = video_info or self.video_info()

        def get_content(url, **kwargs):
            if '/x/web-interface/view?' in url:
                return json.dumps({'code': 0, 'message': 'OK', 'data': video_info})
            if '/x/player/playurl?' in url:
                return json.dumps(copy.deepcopy(self.playinfo()))
            if '/x/player/wbi/v2?' in url:
                return json.dumps({'code': -400, 'message': 'request error'})
            if url.startswith('https://comment.bilibili.com/'):
                return '<i></i>'
            if url.startswith(self.video_url):
                raise AssertionError('the standard video webpage must not be requested')
            raise AssertionError('unexpected URL: %s' % url)

        return get_content

    @staticmethod
    def url_size(url, **kwargs):
        sizes = {
            'https://cdn.example/video-112.m4s': 1000,
            'https://cdn.example/video-16.m4s': 500,
            'https://cdn.example/audio-30280.m4s': 300,
            'https://cdn.example/audio-30232.m4s': 200,
            'https://cdn.example/audio-30216.m4s': 100,
        }
        return sizes[url]

    def test_standard_video_uses_api_and_exposes_audio_only_formats(self):
        extractor = bilibili.Bilibili(self.video_url)
        with patch.object(bilibili, 'get_content', side_effect=self.make_get_content()), \
             patch.object(bilibili.common, 'cookies', object()), \
             patch.object(bilibili.Bilibili, 'url_size', side_effect=self.url_size):
            extractor.prepare()

        self.assertEqual(extractor.title, 'API metadata title')
        self.assertEqual(extractor.danmaku, '<i></i>')
        self.assertEqual(
            extractor.dash_streams['dash-hdflv2-AVC']['src'],
            [
                ['https://cdn.example/video-112.m4s'],
                ['https://cdn.example/audio-30280.m4s'],
            ],
        )
        self.assertEqual(
            extractor.dash_streams['dash-flv360-AVC']['src'],
            [
                ['https://cdn.example/video-16.m4s'],
                ['https://cdn.example/audio-30216.m4s'],
            ],
        )
        self.assertEqual(extractor.streams['dash-audio-30280']['container'], 'm4a')
        self.assertEqual(extractor.streams['dash-audio-30280']['size'], 300)
        self.assertEqual(
            extractor.streams['dash-audio-30280']['src'],
            ['https://cdn.example/audio-30280.m4s'],
        )
        self.assertEqual(extractor.streams['dash-audio-30232']['size'], 200)
        self.assertEqual(extractor.streams['dash-audio-30216']['size'], 100)

    def test_requested_multipart_page_uses_api_page_cid(self):
        pages = [
            {'cid': 111, 'page': 1, 'part': 'First', 'duration': 60},
            {'cid': 222, 'page': 2, 'part': 'Second', 'duration': 60},
        ]
        calls = []
        get_content = self.make_get_content(self.video_info(pages))

        def record_get_content(url, **kwargs):
            calls.append(url)
            return get_content(url, **kwargs)

        extractor = bilibili.Bilibili(self.video_url + '?p=2')
        with patch.object(bilibili, 'get_content', side_effect=record_get_content), \
             patch.object(bilibili.common, 'cookies', object()), \
             patch.object(bilibili.Bilibili, 'url_size', side_effect=self.url_size):
            extractor.prepare()

        self.assertEqual(extractor.title, 'API metadata title (P2. Second)')
        playurl_calls = [url for url in calls if '/x/player/playurl?' in url]
        self.assertTrue(playurl_calls)
        self.assertTrue(all('cid=222' in url for url in playurl_calls))

    def test_requested_audio_skips_unrelated_video_size_probes(self):
        content_calls = []
        size_calls = []
        get_content = self.make_get_content()

        def record_get_content(url, **kwargs):
            content_calls.append(url)
            return get_content(url, **kwargs)

        def record_url_size(url, **kwargs):
            size_calls.append(url)
            return self.url_size(url, **kwargs)

        extractor = bilibili.Bilibili(self.video_url)
        with patch.object(bilibili, 'get_content', side_effect=record_get_content), \
             patch.object(bilibili.common, 'cookies', object()), \
             patch.object(bilibili.Bilibili, 'url_size', side_effect=record_url_size):
            extractor.prepare(stream_id='dash-audio-30280')

        playurl_calls = [url for url in content_calls if '/x/player/playurl?' in url]
        interface_calls = [url for url in content_calls if '/x/player/wbi/v2?' in url]
        self.assertEqual(len(playurl_calls), 1)
        self.assertEqual(interface_calls, [])
        self.assertEqual(size_calls, ['https://cdn.example/audio-30280.m4s'])
        self.assertEqual(set(extractor.streams), {'dash-audio-30280'})
        self.assertEqual(extractor.dash_streams, {})

    def test_metadata_api_error_is_reported_without_none_json_crash(self):
        response = json.dumps({'code': -404, 'message': 'not found', 'data': None})
        extractor = bilibili.Bilibili(self.video_url)
        with patch.object(bilibili, 'get_content', return_value=response):
            with self.assertRaises(SystemExit) as raised:
                extractor.prepare()
        self.assertEqual(raised.exception.code, 1)

    def test_video_url_helpers(self):
        self.assertEqual(
            bilibili.Bilibili.bilibili_view_api('av123'),
            'https://api.bilibili.com/x/web-interface/view?aid=123',
        )
        self.assertEqual(
            bilibili.Bilibili.bilibili_view_api('BV1AbCd'),
            'https://api.bilibili.com/x/web-interface/view?bvid=BV1AbCd',
        )


if __name__ == '__main__':
    unittest.main()
