from json import dumps

import asyncio

from utils.utils import request, StatusError
from tests.curl_data import *

url = "http://127.0.0.1:8080"

"""test_ funcs are skeleton for future pytest"""


async def test_health():
    return await request(url + "/v1/health", headers=headers, method="get")


async def test_fatigue():
    return await request(url + "/v1/drivers/fatigue",
                         headers=headers,
                         data=dumps(drivers_fatigue_data))


async def test_online_hour_start():
    return await request(url + "/v1/drivers/online/hourly",
                         headers=headers,
                         data=dumps(drivers_online_hourly_request_data_start))


async def test_online_hour_final():
    return await request(url + "/v1/drivers/online/hourly",
                         headers=headers,
                         data=dumps(drivers_online_hourly_request_data_final))


async def test_online_quarter_hourly():
    return await request(url + "/v1/drivers/online/quarter_hourly",
                         headers=headers,
                         data=dumps(drivers_online_quarter_hourly_request_data))


async def test_on_order():
    return await request(url + "/v1/drivers/on_order",
                         headers=headers,
                         data=dumps(drivers_on_order_data))


async def all_tests():
    tests = [
        test_health,
        #test_fatigue,
        test_online_hour_start,
        test_online_hour_final,
        test_online_quarter_hourly,
        #test_on_order,
    ]

    for test in tests:
        try:
            print(await test())
        except StatusError:
            print(test.__name__, ": unsuccessful request")


if __name__ == "__main__":
    asyncio.run(all_tests())
