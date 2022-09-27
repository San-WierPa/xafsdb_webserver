# coding: utf-8

"""
    FastAPI

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import xafsdbpy
from xafsdbpy.models.item_response_schema import ItemResponseSchema  # noqa: E501
from xafsdbpy.rest import ApiException

class TestItemResponseSchema(unittest.TestCase):
    """ItemResponseSchema unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ItemResponseSchema
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = xafsdbpy.models.item_response_schema.ItemResponseSchema()  # noqa: E501
        if include_optional :
            return ItemResponseSchema(
                id = 56, 
                file_id = 56, 
                dataset_id = 56
            )
        else :
            return ItemResponseSchema(
                id = 56,
                file_id = 56,
                dataset_id = 56,
        )

    def testItemResponseSchema(self):
        """Test ItemResponseSchema"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
