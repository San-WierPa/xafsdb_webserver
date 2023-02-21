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
from scicat_py.api.users_api import UsersApi  # noqa: E501
from scicat_py.rest import ApiException


class TestUsersApi(unittest.TestCase):
    """UsersApi unit test stubs"""

    def setUp(self):
        self.api = scicat_py.api.users_api.UsersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_users_controller_create_settings(self):
        """Test case for users_controller_create_settings

        """
        pass

    def test_users_controller_find_by_id(self):
        """Test case for users_controller_find_by_id

        """
        pass

    def test_users_controller_get_settings(self):
        """Test case for users_controller_get_settings

        """
        pass

    def test_users_controller_get_user_identity(self):
        """Test case for users_controller_get_user_identity

        """
        pass

    def test_users_controller_get_user_jwt(self):
        """Test case for users_controller_get_user_jwt

        """
        pass

    def test_users_controller_login(self):
        """Test case for users_controller_login

        """
        pass

    def test_users_controller_patch_settings(self):
        """Test case for users_controller_patch_settings

        """
        pass

    def test_users_controller_remove_settings(self):
        """Test case for users_controller_remove_settings

        """
        pass

    def test_users_controller_update_settings(self):
        """Test case for users_controller_update_settings

        """
        pass


if __name__ == '__main__':
    unittest.main()
