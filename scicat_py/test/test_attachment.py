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
from scicat_py.models.attachment import Attachment  # noqa: E501
from scicat_py.rest import ApiException


class TestAttachment(unittest.TestCase):
    """Attachment unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Attachment
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = scicat_py.models.attachment.Attachment()  # noqa: E501
        if include_optional :
            return Attachment(
                owner_group = '0', 
                access_groups = [
                    '0'
                    ], 
                instrument_group = '0', 
                created_by = '0', 
                updated_by = '0', 
                id = '0', 
                thumbnail = '0', 
                caption = '0', 
                dataset_id = '0', 
                proposal_id = '0', 
                sample_id = '0'
            )
        else :
            return Attachment(
                owner_group = '0',
                access_groups = [
                    '0'
                    ],
                created_by = '0',
                updated_by = '0',
                id = '0',
                thumbnail = '0',
                caption = '0',
        )

    def testAttachment(self):
        """Test Attachment"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()