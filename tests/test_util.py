#!/usr/bin/env python

import unittest

from you_get.util.fs import *

class TestUtil(unittest.TestCase):
    def test_legitimize(self):
        self.assertEqual(legitimize("1*2", os="Linux"), "1*2")
        self.assertEqual(legitimize("1*2", os="Darwin"), "1*2")
        self.assertEqual(legitimize("1*2", os="Windows"), "1-2")
