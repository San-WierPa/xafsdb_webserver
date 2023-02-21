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


class UpdateSampleDto(object):
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
        'owner_group': 'str',
        'access_groups': 'list[str]',
        'created_by': 'str',
        'updated_by': 'str',
        'owner': 'str',
        'description': 'str',
        'created_at': 'datetime',
        'sample_characteristics': 'object',
        'is_published': 'bool'
    }

    attribute_map = {
        'owner_group': 'ownerGroup',
        'access_groups': 'accessGroups',
        'created_by': 'createdBy',
        'updated_by': 'updatedBy',
        'owner': 'owner',
        'description': 'description',
        'created_at': 'createdAt',
        'sample_characteristics': 'sampleCharacteristics',
        'is_published': 'isPublished'
    }

    def __init__(self, owner_group=None, access_groups=None, created_by=None, updated_by=None, owner=None, description=None, created_at=None, sample_characteristics=None, is_published=None, local_vars_configuration=None):  # noqa: E501
        """UpdateSampleDto - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._owner_group = None
        self._access_groups = None
        self._created_by = None
        self._updated_by = None
        self._owner = None
        self._description = None
        self._created_at = None
        self._sample_characteristics = None
        self._is_published = None
        self.discriminator = None

        if owner_group is not None:
            self.owner_group = owner_group
        if access_groups is not None:
            self.access_groups = access_groups
        if created_by is not None:
            self.created_by = created_by
        if updated_by is not None:
            self.updated_by = updated_by
        if owner is not None:
            self.owner = owner
        if description is not None:
            self.description = description
        if created_at is not None:
            self.created_at = created_at
        if sample_characteristics is not None:
            self.sample_characteristics = sample_characteristics
        if is_published is not None:
            self.is_published = is_published

    @property
    def owner_group(self):
        """Gets the owner_group of this UpdateSampleDto.  # noqa: E501

        Defines the group which owns the data, and therefore has unrestricted access to this data. Usually a pgroup like p12151  # noqa: E501

        :return: The owner_group of this UpdateSampleDto.  # noqa: E501
        :rtype: str
        """
        return self._owner_group

    @owner_group.setter
    def owner_group(self, owner_group):
        """Sets the owner_group of this UpdateSampleDto.

        Defines the group which owns the data, and therefore has unrestricted access to this data. Usually a pgroup like p12151  # noqa: E501

        :param owner_group: The owner_group of this UpdateSampleDto.  # noqa: E501
        :type: str
        """

        self._owner_group = owner_group

    @property
    def access_groups(self):
        """Gets the access_groups of this UpdateSampleDto.  # noqa: E501

        Optional additional groups which have read access to the data. Users which are member in one of the groups listed here are allowed to access this data. The special group 'public' makes data available to all users  # noqa: E501

        :return: The access_groups of this UpdateSampleDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._access_groups

    @access_groups.setter
    def access_groups(self, access_groups):
        """Sets the access_groups of this UpdateSampleDto.

        Optional additional groups which have read access to the data. Users which are member in one of the groups listed here are allowed to access this data. The special group 'public' makes data available to all users  # noqa: E501

        :param access_groups: The access_groups of this UpdateSampleDto.  # noqa: E501
        :type: list[str]
        """

        self._access_groups = access_groups

    @property
    def created_by(self):
        """Gets the created_by of this UpdateSampleDto.  # noqa: E501

        Functional or user account name who created this instance  # noqa: E501

        :return: The created_by of this UpdateSampleDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this UpdateSampleDto.

        Functional or user account name who created this instance  # noqa: E501

        :param created_by: The created_by of this UpdateSampleDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def updated_by(self):
        """Gets the updated_by of this UpdateSampleDto.  # noqa: E501

        Functional or user account name who last updated this instance  # noqa: E501

        :return: The updated_by of this UpdateSampleDto.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this UpdateSampleDto.

        Functional or user account name who last updated this instance  # noqa: E501

        :param updated_by: The updated_by of this UpdateSampleDto.  # noqa: E501
        :type: str
        """

        self._updated_by = updated_by

    @property
    def owner(self):
        """Gets the owner of this UpdateSampleDto.  # noqa: E501


        :return: The owner of this UpdateSampleDto.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this UpdateSampleDto.


        :param owner: The owner of this UpdateSampleDto.  # noqa: E501
        :type: str
        """

        self._owner = owner

    @property
    def description(self):
        """Gets the description of this UpdateSampleDto.  # noqa: E501


        :return: The description of this UpdateSampleDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateSampleDto.


        :param description: The description of this UpdateSampleDto.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def created_at(self):
        """Gets the created_at of this UpdateSampleDto.  # noqa: E501


        :return: The created_at of this UpdateSampleDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this UpdateSampleDto.


        :param created_at: The created_at of this UpdateSampleDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def sample_characteristics(self):
        """Gets the sample_characteristics of this UpdateSampleDto.  # noqa: E501


        :return: The sample_characteristics of this UpdateSampleDto.  # noqa: E501
        :rtype: object
        """
        return self._sample_characteristics

    @sample_characteristics.setter
    def sample_characteristics(self, sample_characteristics):
        """Sets the sample_characteristics of this UpdateSampleDto.


        :param sample_characteristics: The sample_characteristics of this UpdateSampleDto.  # noqa: E501
        :type: object
        """

        self._sample_characteristics = sample_characteristics

    @property
    def is_published(self):
        """Gets the is_published of this UpdateSampleDto.  # noqa: E501


        :return: The is_published of this UpdateSampleDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_published

    @is_published.setter
    def is_published(self, is_published):
        """Sets the is_published of this UpdateSampleDto.


        :param is_published: The is_published of this UpdateSampleDto.  # noqa: E501
        :type: bool
        """

        self._is_published = is_published

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
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
        if not isinstance(other, UpdateSampleDto):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateSampleDto):
            return True

        return self.to_dict() != other.to_dict()
