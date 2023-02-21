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
from scicat_py.models.create_datablock_dto import CreateDatablockDto  # noqa: E501
from scicat_py.rest import ApiException


class TestCreateDatablockDto(unittest.TestCase):
    """CreateDatablockDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CreateDatablockDto
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = scicat_py.models.create_datablock_dto.CreateDatablockDto()  # noqa: E501
        if include_optional:
            return CreateDatablockDto(
                owner_group="0",
                access_groups=["0"],
                created_by="0",
                updated_by="0",
                dataset_id="0",
                archive_id="0",
                size=1.337,
                packed_size=1.337,
                chk_alg="0",
                version="0",
                data_file_list=[
                    scicat_py.models.data_file.DataFile(
                        path="0",
                        size=1.337,
                        time=datetime.datetime.strptime(
                            "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        chk="0",
                        uid="0",
                        gid="0",
                        perm="0",
                    )
                ],
            )
        else:
            return CreateDatablockDto(
                owner_group="0",
                access_groups=["0"],
                created_by="0",
                updated_by="0",
                dataset_id="0",
                archive_id="0",
                size=1.337,
                packed_size=1.337,
                chk_alg="0",
                version="0",
                data_file_list=[
                    scicat_py.models.data_file.DataFile(
                        path="0",
                        size=1.337,
                        time=datetime.datetime.strptime(
                            "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        chk="0",
                        uid="0",
                        gid="0",
                        perm="0",
                    )
                ],
            )

    def testCreateDatablockDto(self):
        """Test CreateDatablockDto"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
