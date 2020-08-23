# Press Shift+F10 to execute it or replace it with your code.
from fastapi import FastAPI, Header
from config import *
from rest_models import *
from aggregator import Aggregator
from logger.logger import log
from mpc import mpc_strategy
#  uvicorn main:app  --port 8080

app = FastAPI()
aggregator = Aggregator("Fast", 100500)


def init():
    for driver in DRIVERS_DATA:
        name, license_id = driver
        aggregator.add_driver(name, license_id)
    log(aggregator.name, " inited")


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
def v1_drivers_online_hourly(request: DriversOnlineHourlyRequest,
                             x_authorization: str = Header(...),
                             x_request_id: str = Header(...)):
    """как парсить json в кастомный объект"""
    data_extractor = aggregator.drivers_db.get_online_hour
    route = "/v1/drivers/online/hourly"

    headers = {
        "X-Authorization": x_authorization,
        "X-Request-Id": x_request_id,
    }
    return mpc_strategy(headers, request, route, aggregator, data_extractor)


@app.post("/v1/drivers/online/quarter_hourly")
def v1_drivers_online_quarter_hourly(
        request: DriversOnlineQuarterHourlyRequest):
    print(request)
    return SUCCESS


@app.post("/v1/drivers/on_order")
def v1_drivers_on_order(request: DriversOnOrderRequest):
    print(request)
    return SUCCESS


init()
