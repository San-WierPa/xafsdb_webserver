# coding: utf-8

"""
    Dacat API

    SciCat backend API  # noqa: E501

    The version of the OpenAPI document: 4.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import scicat_py
from scicat_py.api.instruments_api import InstrumentsApi  # noqa: E501
from scicat_py.rest import ApiException


class TestInstrumentsApi(unittest.TestCase):
    """InstrumentsApi unit test stubs"""

    def setUp(self):
        self.api = scicat_py.api.instruments_api.InstrumentsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_instruments_controller_create(self):
        """Test case for instruments_controller_create"""
        pass

    def test_instruments_controller_find_all(self):
        """Test case for instruments_controller_find_all"""
        pass

    def test_instruments_controller_find_one(self):
        """Test case for instruments_controller_find_one"""
        pass

    def test_instruments_controller_remove(self):
        """Test case for instruments_controller_remove"""
        pass

    def test_instruments_controller_update(self):
        """Test case for instruments_controller_update"""
        pass


if __name__ == "__main__":
    unittest.main()
