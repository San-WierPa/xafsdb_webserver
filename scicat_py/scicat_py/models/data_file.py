# coding: utf-8

"""
    Dacat API

    SciCat backend API  # noqa: E501

    The version of the OpenAPI document: 4.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from scicat_py.configuration import Configuration


class DataFile(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        "path": "str",
        "size": "float",
        "time": "datetime",
        "chk": "str",
        "uid": "str",
        "gid": "str",
        "perm": "str",
    }

    attribute_map = {
        "path": "path",
        "size": "size",
        "time": "time",
        "chk": "chk",
        "uid": "uid",
        "gid": "gid",
        "perm": "perm",
    }

    def __init__(
        self,
        path=None,
        size=None,
        time=None,
        chk=None,
        uid=None,
        gid=None,
        perm=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """DataFile - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._path = None
        self._size = None
        self._time = None
        self._chk = None
        self._uid = None
        self._gid = None
        self._perm = None
        self.discriminator = None

        self.path = path
        self.size = size
        self.time = time
        self.chk = chk
        self.uid = uid
        self.gid = gid
        self.perm = perm

    @property
    def path(self):
        """Gets the path of this DataFile.  # noqa: E501

        Relative path of the file within the dataset folder  # noqa: E501

        :return: The path of this DataFile.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this DataFile.

        Relative path of the file within the dataset folder  # noqa: E501

        :param path: The path of this DataFile.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and path is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `path`, must not be `None`"
            )  # noqa: E501

        self._path = path

    @property
    def size(self):
        """Gets the size of this DataFile.  # noqa: E501

        Uncompressed file size in bytes  # noqa: E501

        :return: The size of this DataFile.  # noqa: E501
        :rtype: float
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this DataFile.

        Uncompressed file size in bytes  # noqa: E501

        :param size: The size of this DataFile.  # noqa: E501
        :type: float
        """
        if (
            self.local_vars_configuration.client_side_validation and size is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `size`, must not be `None`"
            )  # noqa: E501

        self._size = size

    @property
    def time(self):
        """Gets the time of this DataFile.  # noqa: E501

        Time of file creation on disk, format according to chapter 5.6 internet date/time format in RFC 3339. Local times without timezone/offset info are automatically transformed to UTC using the timezone of the API server  # noqa: E501

        :return: The time of this DataFile.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this DataFile.

        Time of file creation on disk, format according to chapter 5.6 internet date/time format in RFC 3339. Local times without timezone/offset info are automatically transformed to UTC using the timezone of the API server  # noqa: E501

        :param time: The time of this DataFile.  # noqa: E501
        :type: datetime
        """
        if (
            self.local_vars_configuration.client_side_validation and time is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `time`, must not be `None`"
            )  # noqa: E501

        self._time = time

    @property
    def chk(self):
        """Gets the chk of this DataFile.  # noqa: E501

        Checksum for the file, e.g. its sha-2 hashstring  # noqa: E501

        :return: The chk of this DataFile.  # noqa: E501
        :rtype: str
        """
        return self._chk

    @chk.setter
    def chk(self, chk):
        """Sets the chk of this DataFile.

        Checksum for the file, e.g. its sha-2 hashstring  # noqa: E501

        :param chk: The chk of this DataFile.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and chk is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `chk`, must not be `None`"
            )  # noqa: E501

        self._chk = chk

    @property
    def uid(self):
        """Gets the uid of this DataFile.  # noqa: E501

        optional: user ID name as seen on filesystem  # noqa: E501

        :return: The uid of this DataFile.  # noqa: E501
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this DataFile.

        optional: user ID name as seen on filesystem  # noqa: E501

        :param uid: The uid of this DataFile.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and uid is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `uid`, must not be `None`"
            )  # noqa: E501

        self._uid = uid

    @property
    def gid(self):
        """Gets the gid of this DataFile.  # noqa: E501

        optional: group ID name as seen on filesystem  # noqa: E501

        :return: The gid of this DataFile.  # noqa: E501
        :rtype: str
        """
        return self._gid

    @gid.setter
    def gid(self, gid):
        """Sets the gid of this DataFile.

        optional: group ID name as seen on filesystem  # noqa: E501

        :param gid: The gid of this DataFile.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and gid is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `gid`, must not be `None`"
            )  # noqa: E501

        self._gid = gid

    @property
    def perm(self):
        """Gets the perm of this DataFile.  # noqa: E501

        optional: Posix permission bits  # noqa: E501

        :return: The perm of this DataFile.  # noqa: E501
        :rtype: str
        """
        return self._perm

    @perm.setter
    def perm(self, perm):
        """Sets the perm of this DataFile.

        optional: Posix permission bits  # noqa: E501

        :param perm: The perm of this DataFile.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and perm is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `perm`, must not be `None`"
            )  # noqa: E501

        self._perm = perm

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DataFile):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DataFile):
            return True

        return self.to_dict() != other.to_dict()
