# Press Shift+F10 to execute it or replace it with your code.
from fastapi import FastAPI
from rest_models import (
    DriversFatigue,
    DriversOnlineHourlyRequest,
    DriversOnlineQuarterHourlyRequest,
)
from config import SUCCESS, ERROR, DRIVERS_DATA
from aggregator import Aggregator
#  uvicorn main:app  --port 8080

app = FastAPI()
aggregator = Aggregator("Fast", 100500)
for driver in DRIVERS_DATA:
    name, license_id = driver
    aggregator.add_driver(name, license_id)

"""
как забрать все хедеры в Auth
как использовать декоратор для валидации
"""


def _validate_put_request(handler):
    def wrapper(*args, **kwargs):
        headers = args[0]
        xauth = headers.get("X-Authorization", "")
        xreq = headers.get("X-Request-Id", "")
        if xauth == "" or xreq == "":
            return ERROR
        else:
            return handler(*args, **kwargs)
    return wrapper


@app.get("/v1/health")
def v1_health():
    """simple heartbeat"""
    return SUCCESS


@app.post("/v1/drivers/fatigue")
def v1_drivers_fatigue(drivers_fatigue: DriversFatigue):
    """X-Authorization and X-Request-Id required
        stores data of tired drivers
        и что с этим делать?
        допустим пришло:
        {
            "timestamp": "2020-08-11T16:30:25.199",
            "drivers" : [
                {
                    "hash_id": "8xx8",
                    "online": "40",
                    "on_order": "20",
                },
                {
                    "hash_id": "8x7x8",
                    "online": "80",
                    "on_order": "20",
                },
            ]
        }
        какую реакцию запрогить?
        эмулировать блокировку как-то так: self.drivers[hash_id].block()?
        """
    print(drivers_fatigue)
    return SUCCESS


@app.post("/v1/drivers/online/hourly")
def v1_drivers_online_hourly(request: DriversOnlineHourlyRequest):
    print(request)
    return SUCCESS


@app.post("/v1/drivers/online/quarter_hourly")
def v1_drivers_online_quarter_hourly(
        request: DriversOnlineQuarterHourlyRequest):
    print(request)
    return SUCCESS


@app.post("/v1/drivers/on_order")
def v1_drivers_on_order():
    return SUCCESS
