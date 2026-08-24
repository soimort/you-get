#!/usr/bin/env python

import json
import unittest

from you_get.extractors import twitter


class TestTwitter(unittest.TestCase):
    def test_tweet_id_accepts_x_and_twitter_aliases(self):
        item_id = '1530516552084234244'
        urls = [
            'https://x.com/example/status/' + item_id,
            'https://www.x.com/example/status/' + item_id + '/video/1',
            'https://twitter.com/example/status/' + item_id,
            'https://mobile.twitter.com/example/status/' + item_id
        ]

        self.assertEqual([twitter._tweet_id(url) for url in urls], [item_id] * 4)

    def test_xquik_info_uses_key_and_normalizes_downloadable_media(self):
        calls = []

        def fetch(url, headers):
            calls.append((url, headers))
            return json.dumps({
                'tweet': {
                    'media': [
                        {
                            'id': 'photo-id',
                            'type': 'photo',
                            'mediaUrl': 'https://pbs.twimg.com/media/photo?format=png'
                        },
                        {
                            'type': 'video',
                            'videoVariants': [
                                {
                                    'bitrate': 256000,
                                    'contentType': 'video/mp4',
                                    'url': 'https://video.twimg.com/video/low.mp4'
                                },
                                {
                                    'contentType': 'application/x-mpegURL',
                                    'url': 'https://video.twimg.com/video/master.m3u8'
                                },
                                {
                                    'bitrate': 832000,
                                    'contentType': 'video/mp4',
                                    'url': 'https://video.twimg.com/video/high.mp4?tag=12'
                                }
                            ]
                        },
                        {'type': 'video', 'videoVariants': []},
                        {'type': 'unknown', 'mediaUrl': 'https://example.com/file'}
                    ]
                }
            })

        info = twitter._xquik_info('123456789012345', 'api-key', fetch=fetch)

        self.assertEqual(calls, [(
            'https://xquik.com/api/v1/x/tweets/123456789012345',
            {'x-api-key': 'api-key'}
        )])
        self.assertEqual(info, {
            'photos': [{
                'url': 'https://pbs.twimg.com/media/photo?format=png',
                'download_url': 'https://pbs.twimg.com/media/photo?format=png'
            }],
            'mediaDetails': [{
                'video_info': {
                    'variants': [
                        {
                            'bitrate': 256000,
                            'content_type': 'video/mp4',
                            'url': 'https://video.twimg.com/video/low.mp4'
                        },
                        {
                            'bitrate': 832000,
                            'content_type': 'video/mp4',
                            'url': 'https://video.twimg.com/video/high.mp4?tag=12'
                        }
                    ]
                }
            }]
        })


if __name__ == '__main__':
    unittest.main()
