#!/usr/bin/env python

import unittest

from you_get.util.strings import *

class TestStrings(unittest.TestCase):
    def test_safe_chars_simple(self):
        self.assertEqual('', safe_chars('', encoding='utf-8'))
        self.assertEqual('abc', safe_chars('abc', encoding='utf-8'))

    def test_safe_chars_replace(self):
        self.assertEqual('a?c', safe_chars('a\u20ACc', encoding='ascii'))