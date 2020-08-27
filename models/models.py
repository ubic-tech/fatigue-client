from pydantic import BaseModel
from typing import List


class ServerResponse(BaseModel):
    code: str
    message: str


class Endpoint(BaseModel):
    id: str
    endpoint: str


class EndpointResponse(BaseModel):
    endpoints: List[Endpoint]


class DriverData(BaseModel):
    hash_id: str
    share: int


class Drivers(BaseModel):
    timestamp: str
    chain: List[str]


class OnlineHourly(Drivers):
    drivers: List[DriverData]


class OnlineQuarterHourly(OnlineHourly):
    pass


class OnOrder(OnlineHourly):
    pass


class DriverFatigue(BaseModel):
    hash_id: str
    online: int
    on_order: int


class DriversFatigue(BaseModel):
    timestamp: str
    drivers: List[DriverFatigue]
