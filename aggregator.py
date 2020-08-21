from driversDB import DriversDB
from fastapi import FastAPI, Header

ERROR = {'code': "503", 'message': "NOT OK"}
SUCCESS = {'code': "200", 'message': "OK"}


class Router:
    def __init__(self, path, methods, endpoint_name):
        self.path = path
        self.methods = methods
        self.endpoint_name = endpoint_name


ROUTE_MAP = [
    # route, HTTP method, endpoint (class method)
    Router("/v1/health", ["GET", ],  "v1_health", ),
    # ("/v1/drivers/fatigue",                 "POST", "v1_drivers_fatigue", ),
    # ("/v1/drivers/online/hourly",           "POST", "v1_drivers_online_hourly", ),
    # ("/v1/drivers/online/quarter_hourly",   "POST", "v1_drivers_online_quarter_hourly", ),
    # ("/v1/drivers/on_order",                "POST", "v1_drivers_on_order", ),
]


class Aggregator(FastAPI):
    def __init__(self, name, _id, route_map, *args, **kwargs):
        FastAPI.__init__(self)
        self.name = name
        self.id = _id
        self.drivers = DriversDB(*args, **kwargs)

        for route in route_map:
            self.add_api_route(path=route.path,
                               endpoint=getattr(Aggregator, route.endpoint_name),
                               methods=route.methods)

    def add_driver(self, full_name, license_id):
        self.drivers.add_driver(full_name, license_id)

    @staticmethod
    async def v1_health(x_authorization: str = Header(...)):
        print(x_authorization)
        return SUCCESS
