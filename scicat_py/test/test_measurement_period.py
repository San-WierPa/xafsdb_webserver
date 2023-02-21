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
from scicat_py.models.measurement_period import MeasurementPeriod  # noqa: E501
from scicat_py.rest import ApiException


class TestMeasurementPeriod(unittest.TestCase):
    """MeasurementPeriod unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MeasurementPeriod
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = scicat_py.models.measurement_period.MeasurementPeriod()  # noqa: E501
        if include_optional:
            return MeasurementPeriod(
                instrument="0",
                start=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                end=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                comment="0",
            )
        else:
            return MeasurementPeriod(
                instrument="0",
                start=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                end=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                comment="0",
            )

    def testMeasurementPeriod(self):
        """Test MeasurementPeriod"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
