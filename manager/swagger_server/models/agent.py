# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Agent(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, refresh_period: int=None, activated: bool=True, type: str='PASSIVE'):  # noqa: E501
        """Agent - a model defined in Swagger

        :param refresh_period: The refresh_period of this Agent.  # noqa: E501
        :type refresh_period: int
        :param activated: The activated of this Agent.  # noqa: E501
        :type activated: bool
        :param type: The type of this Agent.  # noqa: E501
        :type type: str
        """
        self.swagger_types = {
            'refresh_period': int,
            'activated': bool,
            'type': str
        }

        self.attribute_map = {
            'refresh_period': 'refresh_period',
            'activated': 'activated',
            'type': 'type'
        }

        self._refresh_period = refresh_period
        self._activated = activated
        self._type = type

    @classmethod
    def from_dict(cls, dikt) -> 'Agent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The agent of this Agent.  # noqa: E501
        :rtype: Agent
        """
        return util.deserialize_model(dikt, cls)

    @property
    def refresh_period(self) -> int:
        """Gets the refresh_period of this Agent.

        period of time to collect data for passive monitoring  # noqa: E501

        :return: The refresh_period of this Agent.
        :rtype: int
        """
        return self._refresh_period

    @refresh_period.setter
    def refresh_period(self, refresh_period: int):
        """Sets the refresh_period of this Agent.

        period of time to collect data for passive monitoring  # noqa: E501

        :param refresh_period: The refresh_period of this Agent.
        :type refresh_period: int
        """

        self._refresh_period = refresh_period

    @property
    def activated(self) -> bool:
        """Gets the activated of this Agent.

        activate monitoring  # noqa: E501

        :return: The activated of this Agent.
        :rtype: bool
        """
        return self._activated

    @activated.setter
    def activated(self, activated: bool):
        """Sets the activated of this Agent.

        activate monitoring  # noqa: E501

        :param activated: The activated of this Agent.
        :type activated: bool
        """
        if activated is None:
            raise ValueError("Invalid value for `activated`, must not be `None`")  # noqa: E501

        self._activated = activated

    @property
    def type(self) -> str:
        """Gets the type of this Agent.

        monitoring type PASSIVE/ACTIVE  # noqa: E501

        :return: The type of this Agent.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Agent.

        monitoring type PASSIVE/ACTIVE  # noqa: E501

        :param type: The type of this Agent.
        :type type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type
