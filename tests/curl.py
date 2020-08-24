from aio_requests import get, post
from tests.curl_data import *
from json import dumps
import asyncio

url = "http://127.0.0.1:8080"

"""test_ funcs are skeleton for future pytest"""


async def test_v1_health():
    return await get(url + "/v1/health", headers=headers)


async def test_drivers_fatigue():
    return await post(url + "/v1/drivers/fatigue",
                      headers=headers,
                      data=dumps(drivers_fatigue_data))


async def test_drivers_online_hour():
    return await post(url + "/v1/drivers/online/hourly",
                      headers=headers,
                      data=dumps(drivers_online_hourly_request_data))


async def test_drivers_online_quarter_hourly():
    return await post(url + "/v1/drivers/online/quarter_hourly",
                      headers=headers,
                      data=dumps(drivers_online_quarter_hourly_request_data))


async def test_drivers_on_order():
    return await post(url + "/v1/drivers/on_order",
                      headers=headers,
                      data=dumps(drivers_on_order_data))


async def all_tests():
    print(await test_v1_health())
    print(await test_drivers_fatigue())
    print(await test_drivers_online_hour())
    print(await test_drivers_online_quarter_hourly())
    print(await test_drivers_on_order())

if __name__ == "__main__":
    asyncio.run(all_tests())
