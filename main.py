# Press Shift+F10 to execute it or replace it with your code.
from rest_models import DriversFatigue, Auth
from aggregator import Aggregator, ROUTE_MAP, SUCCESS, ERROR

aggregator = Aggregator("city", 100500, ROUTE_MAP)

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


@aggregator.post("/v1/drivers/fatigue")
def v1_drivers_fatigue(drivers_fatigue: DriversFatigue):
    print(drivers_fatigue)
    return SUCCESS


@aggregator.post("/v1/drivers/online/hourly")
def v1_drivers_online_hourly():
    return SUCCESS


@aggregator.post("/v1/drivers/online/quarter_hourly")
def v1_drivers_online_quarter_hourly():
    return SUCCESS


@aggregator.post("/v1/drivers/on_order")
def v1_drivers_on_order():
    return SUCCESS
