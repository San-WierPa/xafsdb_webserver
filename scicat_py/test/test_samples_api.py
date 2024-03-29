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
from scicat_py.api.samples_api import SamplesApi  # noqa: E501
from scicat_py.rest import ApiException


class TestSamplesApi(unittest.TestCase):
    """SamplesApi unit test stubs"""

    def setUp(self):
        self.api = scicat_py.api.samples_api.SamplesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_samples_controller_create(self):
        """Test case for samples_controller_create"""
        pass

    def test_samples_controller_create_attachments(self):
        """Test case for samples_controller_create_attachments"""
        pass

    def test_samples_controller_create_dataset(self):
        """Test case for samples_controller_create_dataset"""
        pass

    def test_samples_controller_find_all(self):
        """Test case for samples_controller_find_all"""
        pass

    def test_samples_controller_find_all_attachments(self):
        """Test case for samples_controller_find_all_attachments"""
        pass

    def test_samples_controller_find_all_datasets(self):
        """Test case for samples_controller_find_all_datasets"""
        pass

    def test_samples_controller_find_by_id(self):
        """Test case for samples_controller_find_by_id"""
        pass

    def test_samples_controller_find_one(self):
        """Test case for samples_controller_find_one"""
        pass

    def test_samples_controller_find_one_attachment_and_remove(self):
        """Test case for samples_controller_find_one_attachment_and_remove"""
        pass

    def test_samples_controller_find_one_attachment_and_update(self):
        """Test case for samples_controller_find_one_attachment_and_update"""
        pass

    def test_samples_controller_find_one_dataset_and_remove(self):
        """Test case for samples_controller_find_one_dataset_and_remove"""
        pass

    def test_samples_controller_find_one_dataset_and_update(self):
        """Test case for samples_controller_find_one_dataset_and_update"""
        pass

    def test_samples_controller_fullquery(self):
        """Test case for samples_controller_fullquery"""
        pass

    def test_samples_controller_metadata_keys(self):
        """Test case for samples_controller_metadata_keys"""
        pass

    def test_samples_controller_remove(self):
        """Test case for samples_controller_remove"""
        pass

    def test_samples_controller_update(self):
        """Test case for samples_controller_update"""
        pass


if __name__ == "__main__":
    unittest.main()
