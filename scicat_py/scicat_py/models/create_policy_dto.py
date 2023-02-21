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


class CreatePolicyDto(object):
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
        "manager": "list[str]",
        "tape_redundancy": "str",
        "auto_archive": "bool",
        "auto_archive_delay": "float",
        "archive_email_notification": "bool",
        "archive_emails_to_be_notified": "list[str]",
        "retrieve_email_notification": "bool",
        "retrieve_emails_to_be_notified": "list[str]",
        "embargo_period": "float",
    }

    attribute_map = {
        "owner_group": "ownerGroup",
        "access_groups": "accessGroups",
        "created_by": "createdBy",
        "updated_by": "updatedBy",
        "manager": "manager",
        "tape_redundancy": "tapeRedundancy",
        "auto_archive": "autoArchive",
        "auto_archive_delay": "autoArchiveDelay",
        "archive_email_notification": "archiveEmailNotification",
        "archive_emails_to_be_notified": "archiveEmailsToBeNotified",
        "retrieve_email_notification": "retrieveEmailNotification",
        "retrieve_emails_to_be_notified": "retrieveEmailsToBeNotified",
        "embargo_period": "embargoPeriod",
    }

    def __init__(
        self,
        owner_group=None,
        access_groups=None,
        created_by=None,
        updated_by=None,
        manager=None,
        tape_redundancy=None,
        auto_archive=None,
        auto_archive_delay=None,
        archive_email_notification=None,
        archive_emails_to_be_notified=None,
        retrieve_email_notification=None,
        retrieve_emails_to_be_notified=None,
        embargo_period=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """CreatePolicyDto - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._owner_group = None
        self._access_groups = None
        self._created_by = None
        self._updated_by = None
        self._manager = None
        self._tape_redundancy = None
        self._auto_archive = None
        self._auto_archive_delay = None
        self._archive_email_notification = None
        self._archive_emails_to_be_notified = None
        self._retrieve_email_notification = None
        self._retrieve_emails_to_be_notified = None
        self._embargo_period = None
        self.discriminator = None

        self.owner_group = owner_group
        self.access_groups = access_groups
        self.created_by = created_by
        self.updated_by = updated_by
        self.manager = manager
        self.tape_redundancy = tape_redundancy
        self.auto_archive = auto_archive
        self.auto_archive_delay = auto_archive_delay
        self.archive_email_notification = archive_email_notification
        self.archive_emails_to_be_notified = archive_emails_to_be_notified
        self.retrieve_email_notification = retrieve_email_notification
        self.retrieve_emails_to_be_notified = retrieve_emails_to_be_notified
        self.embargo_period = embargo_period

    @property
    def owner_group(self):
        """Gets the owner_group of this CreatePolicyDto.  # noqa: E501

        Defines the group which owns the data, and therefore has unrestricted access to this data. Usually a pgroup like p12151  # noqa: E501

        :return: The owner_group of this CreatePolicyDto.  # noqa: E501
        :rtype: str
        """
        return self._owner_group

    @owner_group.setter
    def owner_group(self, owner_group):
        """Sets the owner_group of this CreatePolicyDto.

        Defines the group which owns the data, and therefore has unrestricted access to this data. Usually a pgroup like p12151  # noqa: E501

        :param owner_group: The owner_group of this CreatePolicyDto.  # noqa: E501
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
        """Gets the access_groups of this CreatePolicyDto.  # noqa: E501

        Optional additional groups which have read access to the data. Users which are member in one of the groups listed here are allowed to access this data. The special group 'public' makes data available to all users  # noqa: E501

        :return: The access_groups of this CreatePolicyDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._access_groups

    @access_groups.setter
    def access_groups(self, access_groups):
        """Sets the access_groups of this CreatePolicyDto.

        Optional additional groups which have read access to the data. Users which are member in one of the groups listed here are allowed to access this data. The special group 'public' makes data available to all users  # noqa: E501

        :param access_groups: The access_groups of this CreatePolicyDto.  # noqa: E501
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
        """Gets the created_by of this CreatePolicyDto.  # noqa: E501

        Functional or user account name who created this instance  # noqa: E501

        :return: The created_by of this CreatePolicyDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this CreatePolicyDto.

        Functional or user account name who created this instance  # noqa: E501

        :param created_by: The created_by of this CreatePolicyDto.  # noqa: E501
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
        """Gets the updated_by of this CreatePolicyDto.  # noqa: E501

        Functional or user account name who last updated this instance  # noqa: E501

        :return: The updated_by of this CreatePolicyDto.  # noqa: E501
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """Sets the updated_by of this CreatePolicyDto.

        Functional or user account name who last updated this instance  # noqa: E501

        :param updated_by: The updated_by of this CreatePolicyDto.  # noqa: E501
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
    def manager(self):
        """Gets the manager of this CreatePolicyDto.  # noqa: E501


        :return: The manager of this CreatePolicyDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._manager

    @manager.setter
    def manager(self, manager):
        """Sets the manager of this CreatePolicyDto.


        :param manager: The manager of this CreatePolicyDto.  # noqa: E501
        :type: list[str]
        """
        if (
            self.local_vars_configuration.client_side_validation and manager is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `manager`, must not be `None`"
            )  # noqa: E501

        self._manager = manager

    @property
    def tape_redundancy(self):
        """Gets the tape_redundancy of this CreatePolicyDto.  # noqa: E501


        :return: The tape_redundancy of this CreatePolicyDto.  # noqa: E501
        :rtype: str
        """
        return self._tape_redundancy

    @tape_redundancy.setter
    def tape_redundancy(self, tape_redundancy):
        """Sets the tape_redundancy of this CreatePolicyDto.


        :param tape_redundancy: The tape_redundancy of this CreatePolicyDto.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation
            and tape_redundancy is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `tape_redundancy`, must not be `None`"
            )  # noqa: E501

        self._tape_redundancy = tape_redundancy

    @property
    def auto_archive(self):
        """Gets the auto_archive of this CreatePolicyDto.  # noqa: E501


        :return: The auto_archive of this CreatePolicyDto.  # noqa: E501
        :rtype: bool
        """
        return self._auto_archive

    @auto_archive.setter
    def auto_archive(self, auto_archive):
        """Sets the auto_archive of this CreatePolicyDto.


        :param auto_archive: The auto_archive of this CreatePolicyDto.  # noqa: E501
        :type: bool
        """
        if (
            self.local_vars_configuration.client_side_validation
            and auto_archive is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `auto_archive`, must not be `None`"
            )  # noqa: E501

        self._auto_archive = auto_archive

    @property
    def auto_archive_delay(self):
        """Gets the auto_archive_delay of this CreatePolicyDto.  # noqa: E501


        :return: The auto_archive_delay of this CreatePolicyDto.  # noqa: E501
        :rtype: float
        """
        return self._auto_archive_delay

    @auto_archive_delay.setter
    def auto_archive_delay(self, auto_archive_delay):
        """Sets the auto_archive_delay of this CreatePolicyDto.


        :param auto_archive_delay: The auto_archive_delay of this CreatePolicyDto.  # noqa: E501
        :type: float
        """
        if (
            self.local_vars_configuration.client_side_validation
            and auto_archive_delay is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `auto_archive_delay`, must not be `None`"
            )  # noqa: E501

        self._auto_archive_delay = auto_archive_delay

    @property
    def archive_email_notification(self):
        """Gets the archive_email_notification of this CreatePolicyDto.  # noqa: E501


        :return: The archive_email_notification of this CreatePolicyDto.  # noqa: E501
        :rtype: bool
        """
        return self._archive_email_notification

    @archive_email_notification.setter
    def archive_email_notification(self, archive_email_notification):
        """Sets the archive_email_notification of this CreatePolicyDto.


        :param archive_email_notification: The archive_email_notification of this CreatePolicyDto.  # noqa: E501
        :type: bool
        """
        if (
            self.local_vars_configuration.client_side_validation
            and archive_email_notification is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `archive_email_notification`, must not be `None`"
            )  # noqa: E501

        self._archive_email_notification = archive_email_notification

    @property
    def archive_emails_to_be_notified(self):
        """Gets the archive_emails_to_be_notified of this CreatePolicyDto.  # noqa: E501


        :return: The archive_emails_to_be_notified of this CreatePolicyDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._archive_emails_to_be_notified

    @archive_emails_to_be_notified.setter
    def archive_emails_to_be_notified(self, archive_emails_to_be_notified):
        """Sets the archive_emails_to_be_notified of this CreatePolicyDto.


        :param archive_emails_to_be_notified: The archive_emails_to_be_notified of this CreatePolicyDto.  # noqa: E501
        :type: list[str]
        """
        if (
            self.local_vars_configuration.client_side_validation
            and archive_emails_to_be_notified is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `archive_emails_to_be_notified`, must not be `None`"
            )  # noqa: E501

        self._archive_emails_to_be_notified = archive_emails_to_be_notified

    @property
    def retrieve_email_notification(self):
        """Gets the retrieve_email_notification of this CreatePolicyDto.  # noqa: E501


        :return: The retrieve_email_notification of this CreatePolicyDto.  # noqa: E501
        :rtype: bool
        """
        return self._retrieve_email_notification

    @retrieve_email_notification.setter
    def retrieve_email_notification(self, retrieve_email_notification):
        """Sets the retrieve_email_notification of this CreatePolicyDto.


        :param retrieve_email_notification: The retrieve_email_notification of this CreatePolicyDto.  # noqa: E501
        :type: bool
        """
        if (
            self.local_vars_configuration.client_side_validation
            and retrieve_email_notification is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `retrieve_email_notification`, must not be `None`"
            )  # noqa: E501

        self._retrieve_email_notification = retrieve_email_notification

    @property
    def retrieve_emails_to_be_notified(self):
        """Gets the retrieve_emails_to_be_notified of this CreatePolicyDto.  # noqa: E501


        :return: The retrieve_emails_to_be_notified of this CreatePolicyDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._retrieve_emails_to_be_notified

    @retrieve_emails_to_be_notified.setter
    def retrieve_emails_to_be_notified(self, retrieve_emails_to_be_notified):
        """Sets the retrieve_emails_to_be_notified of this CreatePolicyDto.


        :param retrieve_emails_to_be_notified: The retrieve_emails_to_be_notified of this CreatePolicyDto.  # noqa: E501
        :type: list[str]
        """
        if (
            self.local_vars_configuration.client_side_validation
            and retrieve_emails_to_be_notified is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `retrieve_emails_to_be_notified`, must not be `None`"
            )  # noqa: E501

        self._retrieve_emails_to_be_notified = retrieve_emails_to_be_notified

    @property
    def embargo_period(self):
        """Gets the embargo_period of this CreatePolicyDto.  # noqa: E501


        :return: The embargo_period of this CreatePolicyDto.  # noqa: E501
        :rtype: float
        """
        return self._embargo_period

    @embargo_period.setter
    def embargo_period(self, embargo_period):
        """Sets the embargo_period of this CreatePolicyDto.


        :param embargo_period: The embargo_period of this CreatePolicyDto.  # noqa: E501
        :type: float
        """
        if (
            self.local_vars_configuration.client_side_validation
            and embargo_period is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `embargo_period`, must not be `None`"
            )  # noqa: E501

        self._embargo_period = embargo_period

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
        if not isinstance(other, CreatePolicyDto):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreatePolicyDto):
            return True

        return self.to_dict() != other.to_dict()
