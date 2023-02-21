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
from scicat_py.models.user_settings import UserSettings  # noqa: E501
from scicat_py.rest import ApiException


class TestUserSettings(unittest.TestCase):
    """UserSettings unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test UserSettings
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = scicat_py.models.user_settings.UserSettings()  # noqa: E501
        if include_optional :
            return UserSettings(
                columns = [
                    None
                    ], 
                dataset_count = 1.337, 
                job_count = 1.337, 
                user_id = '0'
            )
        else :
            return UserSettings(
                columns = [
                    None
                    ],
                dataset_count = 1.337,
                job_count = 1.337,
                user_id = '0',
        )

    def testUserSettings(self):
        """Test UserSettings"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
