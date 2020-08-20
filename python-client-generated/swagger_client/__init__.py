# coding: utf-8

# flake8: noqa

"""
    Taxi Aggregator DB Service

    обращения операторов Такси к БД водителей.  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import apis into sdk package
from swagger_client.api.default_api import DefaultApi
# import ApiClient
from swagger_client.api_client import ApiClient
from swagger_client.configuration import Configuration
# import models into sdk package
from swagger_client.models.driver_fatigue import DriverFatigue
from swagger_client.models.driver_hash import DriverHash
from swagger_client.models.driver_quad_data import DriverQuadData
from swagger_client.models.driver_single_data import DriverSingleData
from swagger_client.models.fatigue_body import FatigueBody
from swagger_client.models.hour_response import HourResponse
from swagger_client.models.quarters_response import QuartersResponse
from swagger_client.models.single_data import SingleData
from swagger_client.models.time_request import TimeRequest
