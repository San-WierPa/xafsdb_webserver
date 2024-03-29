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
from scicat_py.models.policy import Policy  # noqa: E501
from scicat_py.rest import ApiException


class TestPolicy(unittest.TestCase):
    """Policy unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Policy
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = scicat_py.models.policy.Policy()  # noqa: E501
        if include_optional:
            return Policy(
                owner_group="0",
                access_groups=["0"],
                instrument_group="0",
                created_by="0",
                updated_by="0",
                id="0",
                manager=["0"],
                tape_redundancy="0",
                auto_archive=True,
                auto_archive_delay=1.337,
                archive_email_notification=True,
                archive_emails_to_be_notified=["0"],
                retrieve_email_notification=True,
                retrieve_emails_to_be_notified=["0"],
                embargo_period=1.337,
            )
        else:
            return Policy(
                owner_group="0",
                access_groups=["0"],
                created_by="0",
                updated_by="0",
                id="0",
                manager=["0"],
                tape_redundancy="0",
                auto_archive=True,
                auto_archive_delay=1.337,
                archive_email_notification=True,
                archive_emails_to_be_notified=["0"],
                retrieve_email_notification=True,
                retrieve_emails_to_be_notified=["0"],
                embargo_period=1.337,
            )

    def testPolicy(self):
        """Test Policy"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
