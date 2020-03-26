# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.admin_model_system import AdminModelSystem  # noqa: E501
from swagger_server.models.delete_agent import DeleteAgent  # noqa: E501
from swagger_server.models.update_model_vnf import UpdateModelVnf  # noqa: E501
from swagger_server.test import BaseTestCase


class TestVNFManagerController(BaseTestCase):
    """VNFManagerController integration test stubs"""

    def test_add_agent_vnf(self):
        """Test case for add_agent_vnf

        Add new VM and CNT monitoring agent
        """
        payload = AdminModelSystem()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/VNFManager',
            method='POST',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_agent_vnf(self):
        """Test case for delete_agent_vnf

        Stop and delete VM AND CNT monitoring agent
        """
        payload = DeleteAgent()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/VNFManager',
            method='DELETE',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_disable_agent_vnf(self):
        """Test case for disable_agent_vnf

        Stop a VM and CNT monitoring agent
        """
        payload = DeleteAgent()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/VNFManager/disable',
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_enable_agent_vnf(self):
        """Test case for enable_agent_vnf

        Start a VM and CNT monitoring agent
        """
        payload = DeleteAgent()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/VNFManager/enable',
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_agent_vnf(self):
        """Test case for update_agent_vnf

        Update the configuration of a VM and CNT agent
        """
        payload = UpdateModelVnf()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/VNFManager/update',
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
