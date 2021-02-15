# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

import unittest


class test_network(unittest.TestCase):
    def test_network(self):
        from jsbc.Toolbox import SettingsClass
        import jsbc.network

        assert type(jsbc.network.settings) == SettingsClass
