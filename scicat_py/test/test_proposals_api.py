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
from scicat_py.api.proposals_api import ProposalsApi  # noqa: E501
from scicat_py.rest import ApiException


class TestProposalsApi(unittest.TestCase):
    """ProposalsApi unit test stubs"""

    def setUp(self):
        self.api = scicat_py.api.proposals_api.ProposalsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_proposals_controller_create(self):
        """Test case for proposals_controller_create"""
        pass

    def test_proposals_controller_create_attachment(self):
        """Test case for proposals_controller_create_attachment"""
        pass

    def test_proposals_controller_create_dataset(self):
        """Test case for proposals_controller_create_dataset"""
        pass

    def test_proposals_controller_find_all(self):
        """Test case for proposals_controller_find_all"""
        pass

    def test_proposals_controller_find_all_attachments(self):
        """Test case for proposals_controller_find_all_attachments"""
        pass

    def test_proposals_controller_find_all_datasets(self):
        """Test case for proposals_controller_find_all_datasets"""
        pass

    def test_proposals_controller_find_one(self):
        """Test case for proposals_controller_find_one"""
        pass

    def test_proposals_controller_find_one_attachment_and_remove(self):
        """Test case for proposals_controller_find_one_attachment_and_remove"""
        pass

    def test_proposals_controller_find_one_attachment_and_update(self):
        """Test case for proposals_controller_find_one_attachment_and_update"""
        pass

    def test_proposals_controller_find_one_dataset_and_remove(self):
        """Test case for proposals_controller_find_one_dataset_and_remove"""
        pass

    def test_proposals_controller_find_one_dataset_and_update(self):
        """Test case for proposals_controller_find_one_dataset_and_update"""
        pass

    def test_proposals_controller_fullfacet(self):
        """Test case for proposals_controller_fullfacet"""
        pass

    def test_proposals_controller_fullquery(self):
        """Test case for proposals_controller_fullquery"""
        pass

    def test_proposals_controller_remove(self):
        """Test case for proposals_controller_remove"""
        pass

    def test_proposals_controller_update(self):
        """Test case for proposals_controller_update"""
        pass


if __name__ == "__main__":
    unittest.main()
