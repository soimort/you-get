#!/usr/bin/env python

import unittest
from unittest.mock import Mock, patch

import you_get.common as common
from you_get.common import *

class TestCommon(unittest.TestCase):
    
    def test_match1(self):
        self.assertEqual(match1('http://youtu.be/1234567890A', r'youtu.be/([^/]+)'), '1234567890A')
        self.assertEqual(match1('http://youtu.be/1234567890A', r'youtu.be/([^/]+)', r'youtu.(\w+)'), ['1234567890A', 'be'])

    def test_url_size_passes_timeout_and_closes_response(self):
        response = Mock()
        response.headers = {'content-length': '123'}
        with patch.object(common, 'urlopen_with_retry', return_value=response) as urlopen:
            self.assertEqual(common.url_size('https://example.com/file', timeout=5), 123)
        self.assertEqual(urlopen.call_args.kwargs, {'timeout': 5})
        response.close.assert_called_once_with()
