#!/usr/bin/env python

from typing import Any
import unittest
from unittest import mock

from you_get.common import *

class TestCommon(unittest.TestCase):
    
    def test_match1(self):
        self.assertEqual(match1('http://youtu.be/1234567890A', r'youtu.be/([^/]+)'), '1234567890A')
        self.assertEqual(match1('http://youtu.be/1234567890A', r'youtu.be/([^/]+)', r'youtu.(\w+)'), ['1234567890A', 'be'])

#Ensure google_search backup essentailly work 
    def test_google_search(self):
        self.assertIsNotNone(google_search('anyString'))


if __name__ == '__main__':
    unittest.main()