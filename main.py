# Press Shift+F10 to execute it or replace it with your code.
from fastapi import FastAPI, Header
from rest_models import *
from aggregator import Aggregator
from logger.logger import log
from mpc import get_rand_pair
from utils import *
from json import dumps, JSONEncoder
from collections import namedtuple

"""
как забрать все хедеры в Auth
как использовать декоратор для валидации
"""
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
    try:
        self_index = request.chain.index(aggregator.id)  # get index of aggr in chain
    except ValueError:
        return ERROR

    headers = {
        "X-Authorization": x_authorization,
        "X-Request-Id": x_request_id,
    }

    try:
        next_aggr_hash_id = request.chain[self_index + 1]
        next_aggr_url = get_endpoint_url_by_hash(next_aggr_hash_id, x_authorization)
    except IndexError:  # means this is the last aggregator in the chain
        for i, driver in enumerate(request.drivers):
            driver_data = aggregator.drivers_db.get_online_hour(driver.hash_id, request.timestamp)
            request.drivers[i].shares[0] += driver_data   # simply send ubic our share
        r = send(UBIC_URL + V1_SHARES, headers, data=dumps(request))
        if r is None:
            pass
        return SUCCESS

    ubic_shares = []
    for i, driver in enumerate(request.drivers):
        driver_data = aggregator.drivers_db.get_online_hour(driver.hash_id, request.timestamp)
        ubic_share, common_share = get_rand_pair(int(driver_data))
        request.drivers[i].shares[0] += common_share  # only one share is expected for each driver
        dd = DriverData()
        dd.hash_id = driver.hash_id
        dd.shares = [ubic_share, ]
        ubic_shares.append(dd)

    r = send(UBIC_URL + V1_SHARES, headers, data=dumps(ubic_shares))
    if r is None:  # handle errors
        return ERROR

    r = send(next_aggr_url + "/v1/drivers/online/hourly",  # todo: replace the route with var
             headers=headers,
             data=dumps(request))
    if r is None:  # handle errors
        return ERROR
    return SUCCESS


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
