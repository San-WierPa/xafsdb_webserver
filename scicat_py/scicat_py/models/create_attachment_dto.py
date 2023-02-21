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


class CreateAttachmentDto(object):
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
        "owner_group": "str",
        "access_groups": "list[str]",
        "created_by": "str",
        "updated_by": "str",
        "thumbnail": "str",
        "caption": "str",
        "dataset_id": "str",
        "proposal_id": "str",
        "sample_id": "str",
    }

    attribute_map = {
        "owner_group": "ownerGroup",
        "access_groups": "accessGroups",
        "created_by": "createdBy",
        "updated_by": "updatedBy",
        "thumbnail": "thumbnail",
        "caption": "caption",
        "dataset_id": "datasetId",
        "proposal_id": "proposalId",
        "sample_id": "sampleId",
    }

    def __init__(
        self,
        owner_group=None,
        access_groups=None,
        created_by=None,
        updated_by=None,
        thumbnail=None,
        caption=None,
        dataset_id=None,
        proposal_id=None,
        sample_id=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """CreateAttachmentDto - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._owner_group = None
        self._access_groups = None
        self._created_by = None
        self._updated_by = None
        self._thumbnail = None
        self._caption = None
        self._dataset_id = None
        self._proposal_id = None
        self._sample_id = None
        self.discriminator = None

        self.owner_group = owner_group
        self.access_groups = access_groups
        self.created_by = created_by
        self.updated_by = updated_by
        self.thumbnail = thumbnail
        self.caption = caption
        if dataset_id is not None:
            self.dataset_id = dataset_id
        if proposal_id is not None:
            self.proposal_id = proposal_id
        if sample_id is not None:
            self.sample_id = sample_id

    @property
    def owner_group(self):
        """Gets the owner_group of this CreateAttachmentDto.  # noqa: E501

        Defines the group which owns the data, and therefore has unrestricted access to this data. Usually a pgroup like p12151  # noqa: E501

        :return: The owner_group of this CreateAttachmentDto.  # noqa: E501
        :rtype: str
        """
        return self._owner_group

    @owner_group.setter
    def owner_group(self, owner_group):
        """Sets the owner_group of this CreateAttachmentDto.

        Defines the group which owns the data, and therefore has unrestricted access to this data. Usually a pgroup like p12151  # noqa: E501

        :param owner_group: The owner_group of this CreateAttachmentDto.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and owner_group is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `owner_group`, must not be `None`"
            )  # noqa: E501

        self._owner_group = owner_group

    @property
    def access_groups(self):
        """Gets the access_groups of this CreateAttachmentDto.  # noqa: E501

        Optional additional groups which have read access to the data. Users which are member in one of the groups listed here are allowed to access this data. The special group 'public' makes data available to all users  # noqa: E501

        :return: The access_groups of this CreateAttachmentDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._access_groups

    @access_groups.setter
    def access_groups(self, access_groups):
        """Sets the access_groups of this CreateAttachmentDto.

        Optional additional groups which have read access to the data. Users which are member in one of the groups listed here are allowed to access this data. The special group 'public' makes data available to all users  # noqa: E501

        :param access_groups: The access_groups of this CreateAttachmentDto.  # noqa: E501
        :type: list[str]
        """
        if (
            self.local_vars_configuration.client_side_validation
            and access_groups is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `access_groups`, must not be `None`"
            )  # noqa: E501

        self._access_groups = access_groups

    @property
    def created_by(self):
        """Gets the created_by of this CreateAttachmentDto.  # noqa: E501

        Functional or user account name who created this instance  # noqa: E501

        :return: The created_by of this CreateAttachmentDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this CreateAttachmentDto.

        Functional or user account name who created this instance  # noqa: E501

        :param created_by: The created_by of this CreateAttachmentDto.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and created_by is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `created_by`, must not be `None`"
            )  # noqa: E501

        self._created_by = created_by

    @property
    def updated_by(self):
        """Gets the updated_by of this CreateAttachmentDto.  # noqa: E501

        Functional or user account name who last updated this instance  # noqa: E501

        :return: The updated_by of this CreateAttachmentDto.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this CreateAttachmentDto.

        Functional or user account name who last updated this instance  # noqa: E501

        :param updated_by: The updated_by of this CreateAttachmentDto.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and updated_by is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `updated_by`, must not be `None`"
            )  # noqa: E501

        self._updated_by = updated_by

    @property
    def thumbnail(self):
        """Gets the thumbnail of this CreateAttachmentDto.  # noqa: E501

        Contains a thumbnail preview in base64 encoded png format for a given dataset  # noqa: E501

        :return: The thumbnail of this CreateAttachmentDto.  # noqa: E501
        :rtype: str
        """
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, thumbnail):
        """Sets the thumbnail of this CreateAttachmentDto.

        Contains a thumbnail preview in base64 encoded png format for a given dataset  # noqa: E501

        :param thumbnail: The thumbnail of this CreateAttachmentDto.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and thumbnail is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `thumbnail`, must not be `None`"
            )  # noqa: E501

        self._thumbnail = thumbnail

    @property
    def caption(self):
        """Gets the caption of this CreateAttachmentDto.  # noqa: E501

        Attachment caption to show in catanie  # noqa: E501

        :return: The caption of this CreateAttachmentDto.  # noqa: E501
        :rtype: str
        """
        return self._caption

    @caption.setter
    def caption(self, caption):
        """Sets the caption of this CreateAttachmentDto.

        Attachment caption to show in catanie  # noqa: E501

        :param caption: The caption of this CreateAttachmentDto.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and caption is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `caption`, must not be `None`"
            )  # noqa: E501

        self._caption = caption

    @property
    def dataset_id(self):
        """Gets the dataset_id of this CreateAttachmentDto.  # noqa: E501


        :return: The dataset_id of this CreateAttachmentDto.  # noqa: E501
        :rtype: str
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        """Sets the dataset_id of this CreateAttachmentDto.


        :param dataset_id: The dataset_id of this CreateAttachmentDto.  # noqa: E501
        :type: str
        """

        self._dataset_id = dataset_id

    @property
    def proposal_id(self):
        """Gets the proposal_id of this CreateAttachmentDto.  # noqa: E501


        :return: The proposal_id of this CreateAttachmentDto.  # noqa: E501
        :rtype: str
        """
        return self._proposal_id

    @proposal_id.setter
    def proposal_id(self, proposal_id):
        """Sets the proposal_id of this CreateAttachmentDto.


        :param proposal_id: The proposal_id of this CreateAttachmentDto.  # noqa: E501
        :type: str
        """

        self._proposal_id = proposal_id

    @property
    def sample_id(self):
        """Gets the sample_id of this CreateAttachmentDto.  # noqa: E501


        :return: The sample_id of this CreateAttachmentDto.  # noqa: E501
        :rtype: str
        """
        return self._sample_id

    @sample_id.setter
    def sample_id(self, sample_id):
        """Sets the sample_id of this CreateAttachmentDto.


        :param sample_id: The sample_id of this CreateAttachmentDto.  # noqa: E501
        :type: str
        """

        self._sample_id = sample_id

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
        if not isinstance(other, CreateAttachmentDto):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateAttachmentDto):
            return True

        return self.to_dict() != other.to_dict()
