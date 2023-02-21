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
from scicat_py.api.jobs_api import JobsApi  # noqa: E501
from scicat_py.rest import ApiException


class TestJobsApi(unittest.TestCase):
    """JobsApi unit test stubs"""

    def setUp(self):
        self.api = scicat_py.api.jobs_api.JobsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_jobs_controller_create(self):
        """Test case for jobs_controller_create

        """
        pass

    def test_jobs_controller_find_all(self):
        """Test case for jobs_controller_find_all

        """
        pass

    def test_jobs_controller_find_one(self):
        """Test case for jobs_controller_find_one

        """
        pass

    def test_jobs_controller_fullfacet(self):
        """Test case for jobs_controller_fullfacet

        """
        pass

    def test_jobs_controller_fullquery(self):
        """Test case for jobs_controller_fullquery

        """
        pass

    def test_jobs_controller_remove(self):
        """Test case for jobs_controller_remove

        """
        pass

    def test_jobs_controller_update(self):
        """Test case for jobs_controller_update

        """
        pass


if __name__ == '__main__':
    unittest.main()
