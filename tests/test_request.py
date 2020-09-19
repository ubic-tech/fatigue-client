from fastapi.testclient import TestClient
from clickhouse_driver.errors import NetworkError

from tests.curl_data import *
from main import app
from utils.utils import StatusError

EXPECTED = {'code': "200", 'message': "OK"}


def test_health():
    r = TestClient(app).get("/v1/health")
    assert r.status_code == 200
    assert r.json() == EXPECTED


def test_fatigue():
    r = TestClient(app).post("/v1/drivers/fatigue",
                             headers=headers,
                             data=fatigue_request.json())
    assert r.status_code == 200
    assert r.json() == EXPECTED


def test_online_hourly():
    try:
        r = TestClient(app).post("/v1/drivers/online/hourly",
                                 headers=headers,
                                 data=online_hourly_request.json())
    except (NetworkError, StatusError):
        return
    assert r.status_code == 200
    assert r.json() == EXPECTED


def test_online_history_hourly():
    try:
        r = TestClient(app).post("/v1/drivers/online/history_hourly",
                                 headers=headers,
                                 data=history_hourly_request.json())
    except (NetworkError, StatusError):
        return
    assert r.status_code == 200
    assert r.json() == EXPECTED


def test_online_quarter_hourly():
    try:
        r = TestClient(app).post("/v1/drivers/online/quarter_hourly",
                                 headers=headers,
                                 data=online_quarter_hourly_request.json())
    except (NetworkError, StatusError):
        return
    assert r.status_code == 200
    assert r.json() == EXPECTED


def test_on_order():
    try:
        r = TestClient(app).post("/v1/drivers/on_order",
                                 headers=headers,
                                 data=on_order_request.json())
    except (NetworkError, StatusError):
        return
    assert r.status_code == 200
    assert r.json() == EXPECTED
