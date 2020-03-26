# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.db_model import DbModel  # noqa: E501
from swagger_server.models.symptome import Symptome  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSensorController(BaseTestCase):
    """SensorController integration test stubs"""

    def test_add_db_config(self):
        """Test case for add_db_config

        Add database et data flow configuration
        """
        payload = DbModel()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/sensor/configuration',
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
            '/swarmourr/manger/1.0.0/sensor/agents',
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
            '/swarmourr/manger/1.0.0/sensor/collected',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_new_information_stored(self):
        """Test case for new_information_stored

        get notification about new data
        """
        query_string = [('path', 'path_example')]
        response = self.client.open(
            '/swarmourr/manger/1.0.0/sensor/notification',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_new_symptome(self):
        """Test case for send_new_symptome

        send new symptome
        """
        payload = Symptome()
        response = self.client.open(
            '/swarmourr/manger/1.0.0/sensor/symptome',
            method='POST',
            data=json.dumps(payload),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
