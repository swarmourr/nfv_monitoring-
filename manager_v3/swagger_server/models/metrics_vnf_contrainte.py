# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class MetricsVnfContrainte(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, mem: float=None, cpu: float=None):  # noqa: E501
        """MetricsVnfContrainte - a model defined in Swagger

        :param mem: The mem of this MetricsVnfContrainte.  # noqa: E501
        :type mem: float
        :param cpu: The cpu of this MetricsVnfContrainte.  # noqa: E501
        :type cpu: float
        """
        self.swagger_types = {
            'mem': float,
            'cpu': float
        }

        self.attribute_map = {
            'mem': 'mem',
            'cpu': 'cpu'
        }

        self._mem = mem
        self._cpu = cpu

    @classmethod
    def from_dict(cls, dikt) -> 'MetricsVnfContrainte':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The metrics_vnf_contrainte of this MetricsVnfContrainte.  # noqa: E501
        :rtype: MetricsVnfContrainte
        """
        return util.deserialize_model(dikt, cls)

    @property
    def mem(self) -> float:
        """Gets the mem of this MetricsVnfContrainte.

        monitoring  RAM contrainte  # noqa: E501

        :return: The mem of this MetricsVnfContrainte.
        :rtype: float
        """
        return self._mem

    @mem.setter
    def mem(self, mem: float):
        """Sets the mem of this MetricsVnfContrainte.

        monitoring  RAM contrainte  # noqa: E501

        :param mem: The mem of this MetricsVnfContrainte.
        :type mem: float
        """
        if mem is None:
            raise ValueError("Invalid value for `mem`, must not be `None`")  # noqa: E501

        self._mem = mem

    @property
    def cpu(self) -> float:
        """Gets the cpu of this MetricsVnfContrainte.

        monitoring cpu  contrainte  # noqa: E501

        :return: The cpu of this MetricsVnfContrainte.
        :rtype: float
        """
        return self._cpu

    @cpu.setter
    def cpu(self, cpu: float):
        """Sets the cpu of this MetricsVnfContrainte.

        monitoring cpu  contrainte  # noqa: E501

        :param cpu: The cpu of this MetricsVnfContrainte.
        :type cpu: float
        """
        if cpu is None:
            raise ValueError("Invalid value for `cpu`, must not be `None`")  # noqa: E501

        self._cpu = cpu
