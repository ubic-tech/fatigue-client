from requests import get, post
from curl_data import *
from json import dumps

url = " http://127.0.0.1:8080"

"""test_ funcs are skeleton for future pytest"""


def test_v1_health():
    r = get(url + "/v1/health", headers=headers)
    print(r.json())


def test_drivers_fatigue():
    r = post(url + "/v1/drivers/fatigue",
             headers=headers,
             data=dumps(drivers_fatigue_data))
    print(r.json())


def test_drivers_online_hour():
    r = post(url + "/v1/drivers/online/hourly",
             headers=headers,
             data=dumps(drivers_online_hourly_request_data))
    print(r.json())


def test_drivers_online_quarter_hourly():
    r = post(url + "/v1/drivers/online/quarter_hourly",
             headers=headers,
             data=dumps(drivers_online_quarter_hourly_request_data))
    print(r.json())


def test_drivers_on_order():
    r = post(url + "/v1/drivers/on_order",
             headers=headers,
             data=dumps(drivers_on_order_data))
    print(r.json())


if __name__ == "__main__":
    test_v1_health()
    test_drivers_fatigue()
    test_drivers_online_hour()
    test_drivers_online_quarter_hourly()
    test_drivers_on_order()
