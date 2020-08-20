# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.fatigue_body import FatigueBody  # noqa: E501
from swagger_server.models.hour_response import HourResponse  # noqa: E501
from swagger_server.models.quarters_response import QuartersResponse  # noqa: E501
from swagger_server.models.time_request import TimeRequest  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_v1_drivers_fatigue_post(self):
        """Test case for v1_drivers_fatigue_post

        фиксировани усталости водителй
        """
        body = FatigueBody()
        response = self.client.open(
            '/v1/drivers/fatigue',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_v1_drivers_on_order_post(self):
        """Test case for v1_drivers_on_order_post

        Получение информации \"на заказе\" для группы водителей
        """
        body = TimeRequest()
        response = self.client.open(
            '/v1/drivers/on_order',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_v1_drivers_online_hourly_post(self):
        """Test case for v1_drivers_online_hourly_post

        Получение информации \"на линии\" (online) для группы водителей.
        """
        body = TimeRequest()
        response = self.client.open(
            '/v1/drivers/online/hourly',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_v1_drivers_online_quater_hourly_post(self):
        """Test case for v1_drivers_online_quater_hourly_post

        Получение информации \"на линии\" (online) для группы водителей
        """
        body = TimeRequest()
        response = self.client.open(
            '/v1/drivers/online/quater_hourly',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
