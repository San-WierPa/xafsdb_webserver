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
from scicat_py.models.create_job_dto import CreateJobDto  # noqa: E501
from scicat_py.rest import ApiException


class TestCreateJobDto(unittest.TestCase):
    """CreateJobDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CreateJobDto
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = scicat_py.models.create_job_dto.CreateJobDto()  # noqa: E501
        if include_optional:
            return CreateJobDto(
                email_job_initiator="0",
                type="0",
                creation_time=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                execution_time=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                job_params=None,
                job_status_message="0",
                dataset_list=None,
                job_result_object=None,
            )
        else:
            return CreateJobDto(
                email_job_initiator="0",
                type="0",
                creation_time=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
            )

    def testCreateJobDto(self):
        """Test CreateJobDto"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
