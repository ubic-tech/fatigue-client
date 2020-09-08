from fastapi.testclient import TestClient
from tests.curl_data import *
from main import app

client = TestClient(app)
EXPECTED = {'code': "200", 'message': "OK"}


def test_health():
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == EXPECTED


def test_fatigue():
    response = client.post("/v1/drivers/fatigue",
                           headers=headers,
                           json=drivers_fatigue_data)
    assert response.status_code == 200
    assert response.json() == EXPECTED


def test_online_hourly():
    response = client.post("/v1/drivers/online/hourly",
                           headers=headers,
                           json=drivers_online_hourly_request_data)
    assert response.status_code == 200
    assert response.json() == EXPECTED


def test_online_quarter_hourly():
    response = client.post("/v1/drivers/online/quarter_hourly",
                           headers=headers,
                           json=drivers_online_quarter_hourly_request_data)
    assert response.status_code == 200
    assert response.json() == EXPECTED


def test_on_order():
    response = client.post("/v1/drivers/on_order",
                           headers=headers,
                           json=drivers_on_order_data)
    assert response.status_code == 200
    assert response.json() == EXPECTED
