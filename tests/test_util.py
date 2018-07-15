#!/usr/bin/env python

import unittest

from you_get.util.fs import *

class TestUtil(unittest.TestCase):
    def test_legitimize(self):
        self.assertEqual(legitimize("1*2", os="linux"), "1*2")
        self.assertEqual(legitimize("1*2", os="mac"), "1*2")
        self.assertEqual(legitimize("1*2", os="windows"), "1-2")
        self.assertEqual(legitimize("1*2", os="wsl"), "1-2")
