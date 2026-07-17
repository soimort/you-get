#!/usr/bin/env python

import unittest
from unittest.mock import patch

from you_get.extractor import VideoExtractor


class TestVideoExtractor(unittest.TestCase):
    def test_m4a_container_is_preserved_for_audio_only_stream(self):
        extractor = VideoExtractor('https://example.com/audio')
        extractor.title = 'Audio only'
        extractor.streams = {
            'audio': {
                'container': 'm4a',
                'quality': 'audio',
                'size': 123,
                'src': ['https://cdn.example/audio.m4s'],
            },
        }
        extractor.streams_sorted = [{'id': 'audio'}]

        with patch.object(extractor, 'p'), \
             patch('you_get.extractor.download_urls') as download_urls:
            extractor.download(
                stream_id='audio',
                output_dir='.',
                merge=True,
                caption=False,
                keep_obj=True,
            )

        self.assertEqual(download_urls.call_args.args[2], 'm4a')


if __name__ == '__main__':
    unittest.main()
