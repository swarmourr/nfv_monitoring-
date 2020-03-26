# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.db_model import DbModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestServerController(BaseTestCase):
    """ServerController integration test stubs"""

    def test_add_db_config(self):
        """Test case for add_db_config

        Add database et data flow configuration
        """
        payload = DbModel()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/server/configuration',
            method='POST',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_agents(self):
        """Test case for get_all_agents

        Get all agent deployed
        """
        query_string = [('path', 'path_example')]
        response = self.client.open(
            '/swarmourr/manger/1.0.0/server/agents',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_data(self):
        """Test case for get_all_data

        Get all data of an agent
        """
        query_string = [('path', 'path_example')]
        response = self.client.open(
            '/swarmourr/manger/1.0.0/server/collected',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
