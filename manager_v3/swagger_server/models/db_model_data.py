# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class DbModelData(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, flume_url: str='true', port: str='false'):  # noqa: E501
        """DbModelData - a model defined in Swagger

        :param flume_url: The flume_url of this DbModelData.  # noqa: E501
        :type flume_url: str
        :param port: The port of this DbModelData.  # noqa: E501
        :type port: str
        """
        self.swagger_types = {
            'flume_url': str,
            'port': str
        }

        self.attribute_map = {
            'flume_url': 'flume_url',
            'port': 'port'
        }

        self._flume_url = flume_url
        self._port = port

    @classmethod
    def from_dict(cls, dikt) -> 'DbModelData':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The db_model_data of this DbModelData.  # noqa: E501
        :rtype: DbModelData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def flume_url(self) -> str:
        """Gets the flume_url of this DbModelData.

        flume http link  # noqa: E501

        :return: The flume_url of this DbModelData.
        :rtype: str
        """
        return self._flume_url

    @flume_url.setter
    def flume_url(self, flume_url: str):
        """Sets the flume_url of this DbModelData.

        flume http link  # noqa: E501

        :param flume_url: The flume_url of this DbModelData.
        :type flume_url: str
        """
        if flume_url is None:
            raise ValueError("Invalid value for `flume_url`, must not be `None`")  # noqa: E501

        self._flume_url = flume_url

    @property
    def port(self) -> str:
        """Gets the port of this DbModelData.

        flume http port  # noqa: E501

        :return: The port of this DbModelData.
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port: str):
        """Sets the port of this DbModelData.

        flume http port  # noqa: E501

        :param port: The port of this DbModelData.
        :type port: str
        """
        if port is None:
            raise ValueError("Invalid value for `port`, must not be `None`")  # noqa: E501

        self._port = port
