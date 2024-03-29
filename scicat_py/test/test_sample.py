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
from scicat_py.models.sample import Sample  # noqa: E501
from scicat_py.rest import ApiException


class TestSample(unittest.TestCase):
    """Sample unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Sample
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = scicat_py.models.sample.Sample()  # noqa: E501
        if include_optional:
            return Sample(
                owner_group="0",
                access_groups=["0"],
                instrument_group="0",
                created_by="0",
                updated_by="0",
                sample_id="0",
                owner="0",
                description="0",
                created_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                updated_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                sample_characteristics=None,
                is_published=True,
                attachments=[
                    scicat_py.models.attachment.Attachment(
                        owner_group="0",
                        access_groups=["0"],
                        instrument_group="0",
                        created_by="0",
                        updated_by="0",
                        _id="0",
                        thumbnail="0",
                        caption="0",
                        dataset_id="0",
                        proposal_id="0",
                        sample_id="0",
                    )
                ],
                datasets=[
                    scicat_py.models.dataset.Dataset(
                        owner_group="0",
                        access_groups=["0"],
                        instrument_group="0",
                        created_by="0",
                        updated_by="0",
                        pid="0",
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
                        datasetlifecycle=null,
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
                        attachments=[
                            scicat_py.models.attachment.Attachment(
                                owner_group="0",
                                access_groups=["0"],
                                instrument_group="0",
                                created_by="0",
                                updated_by="0",
                                _id="0",
                                thumbnail="0",
                                caption="0",
                                dataset_id="0",
                                proposal_id="0",
                                sample_id="0",
                            )
                        ],
                        origdatablocks=[
                            scicat_py.models.orig_datablock.OrigDatablock(
                                owner_group="0",
                                access_groups=["0"],
                                instrument_group="0",
                                created_by="0",
                                updated_by="0",
                                _id="0",
                                dataset_id="0",
                                size=1.337,
                                data_file_list=["0"],
                            )
                        ],
                        datablocks=[
                            scicat_py.models.datablock.Datablock(
                                owner_group="0",
                                access_groups=["0"],
                                instrument_group="0",
                                created_by="0",
                                updated_by="0",
                                _id="0",
                                dataset_id="0",
                                archive_id="0",
                                size=1.337,
                                packed_size=1.337,
                                chk_alg="0",
                                version="0",
                                data_file_list=["0"],
                            )
                        ],
                    )
                ],
            )
        else:
            return Sample(
                owner_group="0",
                access_groups=["0"],
                created_by="0",
                updated_by="0",
                sample_id="0",
                owner="0",
                description="0",
                created_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                updated_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                sample_characteristics=None,
                is_published=True,
                attachments=[
                    scicat_py.models.attachment.Attachment(
                        owner_group="0",
                        access_groups=["0"],
                        instrument_group="0",
                        created_by="0",
                        updated_by="0",
                        _id="0",
                        thumbnail="0",
                        caption="0",
                        dataset_id="0",
                        proposal_id="0",
                        sample_id="0",
                    )
                ],
                datasets=[
                    scicat_py.models.dataset.Dataset(
                        owner_group="0",
                        access_groups=["0"],
                        instrument_group="0",
                        created_by="0",
                        updated_by="0",
                        pid="0",
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
                        datasetlifecycle=null,
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
                        attachments=[
                            scicat_py.models.attachment.Attachment(
                                owner_group="0",
                                access_groups=["0"],
                                instrument_group="0",
                                created_by="0",
                                updated_by="0",
                                _id="0",
                                thumbnail="0",
                                caption="0",
                                dataset_id="0",
                                proposal_id="0",
                                sample_id="0",
                            )
                        ],
                        origdatablocks=[
                            scicat_py.models.orig_datablock.OrigDatablock(
                                owner_group="0",
                                access_groups=["0"],
                                instrument_group="0",
                                created_by="0",
                                updated_by="0",
                                _id="0",
                                dataset_id="0",
                                size=1.337,
                                data_file_list=["0"],
                            )
                        ],
                        datablocks=[
                            scicat_py.models.datablock.Datablock(
                                owner_group="0",
                                access_groups=["0"],
                                instrument_group="0",
                                created_by="0",
                                updated_by="0",
                                _id="0",
                                dataset_id="0",
                                archive_id="0",
                                size=1.337,
                                packed_size=1.337,
                                chk_alg="0",
                                version="0",
                                data_file_list=["0"],
                            )
                        ],
                    )
                ],
            )

    def testSample(self):
        """Test Sample"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
