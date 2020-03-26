# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.osgi_host import OsgiHost  # noqa: E501
from swagger_server.models.osgi_model_jvm import OsgiModelJvm  # noqa: E501
from swagger_server.test import BaseTestCase


class TestANFManagerController(BaseTestCase):
    """ANFManagerController integration test stubs"""

    def test_add_agent_anf(self):
        """Test case for add_agent_anf

        Add new applicatif  monitoring agent
        """
        payload = OsgiModelJvm()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/ANFManager',
            method='POST',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_agent(self):
        """Test case for delete_agent

        Stop and delete applicatif  monitoring agent
        """
        payload = OsgiHost()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/ANFManager',
            method='DELETE',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_disable_agent(self):
        """Test case for disable_agent

        Stop an applicatif  monitoring agent
        """
        payload = OsgiHost()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/ANFManager/disable',
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_enable_agent(self):
        """Test case for enable_agent

        Start an applicatif monitoring agent
        """
        payload = OsgiHost()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/ANFManager/enable',
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_agent_anf(self):
        """Test case for update_agent_anf

        Update the configuration of an applicatif agent
        """
        payload = OsgiModelJvm()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/ANFManager/update',
            method='PUT',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
