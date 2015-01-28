#!/usr/bin/env python

import unittest

from you_get.util.fs import *

class TestFs(unittest.TestCase):
    def test_legitimize(self):
        self.assertEqual(legitimize("1*2", os="Linux"), "1*2")
        self.assertEqual(legitimize("1*2", os="Darwin"), "1*2")
        self.assertEqual(legitimize("1*2", os="Windows"), "1-2")

    def test_get_filename_simple(self):
        self.assertEqual('name.ext', get_filename('name', 'ext', os='Linux', encoding='utf-8'))

    def test_get_filename_parts(self):
        self.assertEqual('name[02].ext', get_filename('name', 'ext', part=2, os='Linux', encoding='utf-8'))
        self.assertEqual('name(02).ext', get_filename('name', 'ext', part=2, os='Windows', encoding='utf-8'))

    def test_get_filename_encoding_error(self):
        self.assertEqual('name\u20AC.ext', get_filename('name\u20AC', 'ext', os='Linux', encoding='utf-8'))
        self.assertEqual('name\u20AC.ext', get_filename('name\u20AC', 'ext', os='Windows', encoding='utf-8'))
        self.assertEqual('name?.ext', get_filename('name\u20AC', 'ext', os='Linux', encoding='ascii'))
        self.assertEqual('name-.ext', get_filename('name\u20AC', 'ext', os='Windows', encoding='ascii'))

    def test_get_filename_id(self):
        self.assertEqual('name\u20AC.ext', get_filename('name\u20AC', 'ext', os='Linux', id='hi', encoding='utf-8'))
        self.assertEqual('name? - hi.ext', get_filename('name\u20AC', 'ext', os='Linux', id='hi', encoding='ascii'))