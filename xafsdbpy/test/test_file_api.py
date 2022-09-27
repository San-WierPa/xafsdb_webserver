# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import xafsdbpy
from xafsdbpy.api.file_api import FileApi  # noqa: E501
from xafsdbpy.rest import ApiException


class TestFileApi(unittest.TestCase):
    """FileApi unit test stubs"""

    def setUp(self):
        self.api = xafsdbpy.api.file_api.FileApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_api_v1_file_download_get(self):
        """Test case for api_v1_file_download_get

        Api Download File  # noqa: E501
        """
        pass

    def test_api_v1_file_get_get(self):
        """Test case for api_v1_file_get_get

        Api Get File Metadata  # noqa: E501
        """
        pass

    def test_api_v1_file_list_get(self):
        """Test case for api_v1_file_list_get

        Api List Files Metadata  # noqa: E501
        """
        pass

    def test_api_v1_file_upload_post(self):
        """Test case for api_v1_file_upload_post

        Api Upload File  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
