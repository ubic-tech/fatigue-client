from utils import request, StatusError
from tests.curl_data import *
from json import dumps
import asyncio

url = "http://127.0.0.1:8080"

"""test_ funcs are skeleton for future pytest"""


async def test_v1_health():
    return await request(url + "/v1/health", headers=headers, method="get")


async def test_drivers_fatigue():
    return await request(url + "/v1/drivers/fatigue",
                         headers=headers,
                         data=dumps(drivers_fatigue_data))


async def test_drivers_online_hour():
    return await request(url + "/v1/drivers/online/hourly",
                         headers=headers,
                         data=dumps(drivers_online_hourly_request_data))


async def test_drivers_online_quarter_hourly():
    return await request(url + "/v1/drivers/online/quarter_hourly",
                         headers=headers,
                         data=dumps(drivers_online_quarter_hourly_request_data))


async def test_drivers_on_order():
    return await request(url + "/v1/drivers/on_order",
                         headers=headers,
                         data=dumps(drivers_on_order_data))


async def all_tests():
    tests = [
        test_v1_health,
        test_drivers_fatigue,
        test_drivers_online_hour,
        test_drivers_online_quarter_hourly,
        test_drivers_on_order,
    ]

    for test in tests:
        try:
            print(await test())
        except StatusError:
            print(test.__name__, ": unsuccessful request")


if __name__ == "__main__":
    asyncio.run(all_tests())
