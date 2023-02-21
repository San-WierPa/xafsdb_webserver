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
from scicat_py.models.create_dataset_dto import CreateDatasetDto  # noqa: E501
from scicat_py.rest import ApiException


class TestCreateDatasetDto(unittest.TestCase):
    """CreateDatasetDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CreateDatasetDto
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = scicat_py.models.create_dataset_dto.CreateDatasetDto()  # noqa: E501
        if include_optional:
            return CreateDatasetDto(
                owner_group="0",
                access_groups=["0"],
                created_by="0",
                updated_by="0",
                owner="0",
                owner_email="0",
                orcid_of_owner="0",
                contact_email="0",
                source_folder="0",
                source_folder_host="0",
                size=1.337,
                packed_size=1.337,
                number_of_files=1.337,
                number_of_files_archived=1.337,
                creation_time=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                type="0",
                validation_status="0",
                keywords=["0"],
                description="0",
                dataset_name="0",
                classification="0",
                license="0",
                version="0",
                is_published=True,
                history=[None],
                datasetlifecycle=scicat_py.models.lifecycle.Lifecycle(
                    archivable=True,
                    retrievable=True,
                    publishable=True,
                    date_of_disk_purging=datetime.datetime.strptime(
                        "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    archive_retention_time=datetime.datetime.strptime(
                        "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    date_of_publishing=datetime.datetime.strptime(
                        "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    published_on=datetime.datetime.strptime(
                        "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    is_on_central_disk=True,
                    archive_status_message="0",
                    retrieve_status_message="0",
                    archive_return_message=scicat_py.models.archive_return_message.archiveReturnMessage(),
                    retrieve_return_message=scicat_py.models.retrieve_return_message.retrieveReturnMessage(),
                    exported_to="0",
                    retrieve_integrity_check=True,
                ),
                created_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                updated_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                instrument_id="0",
                techniques=[
                    scicat_py.models.technique.Technique(
                        pid="0",
                        name="0",
                    )
                ],
                shared_with=["0"],
                creation_location="0",
                principal_investigator="0",
                scientific_metadata=None,
            )
        else:
            return CreateDatasetDto(
                owner_group="0",
                access_groups=["0"],
                owner="0",
                contact_email="0",
                source_folder="0",
                creation_time=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                type="0",
                dataset_name="0",
                is_published=True,
                creation_location="0",
                principal_investigator="0",
                scientific_metadata=None,
            )

    def testCreateDatasetDto(self):
        """Test CreateDatasetDto"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
