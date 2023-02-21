# coding: utf-8

"""
    Dacat API

    SciCat backend API  # noqa: E501

    The version of the OpenAPI document: 4.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import datetime
import unittest

import scicat_py
from scicat_py.models.credentials_dto import CredentialsDto  # noqa: E501
from scicat_py.rest import ApiException


class TestCredentialsDto(unittest.TestCase):
    """CredentialsDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CredentialsDto
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = scicat_py.models.credentials_dto.CredentialsDto()  # noqa: E501
        if include_optional :
            return CredentialsDto(
                username = '0', 
                password = '0'
            )
        else :
            return CredentialsDto(
                username = '0',
                password = '0',
        )

    def testCredentialsDto(self):
        """Test CredentialsDto"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()