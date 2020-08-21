from pydantic import BaseModel
from typing import List


class DriverData(BaseModel):
    hash_id: str
    shares: List[int]  # 1 or 4 values depending on request/response


class DriversRequest(BaseModel):
    timestamp: str
    chain: str


class DriversOnlineHourlyRequest(DriversRequest):
    drivers: List[DriverData]


class DriverFatigue(BaseModel):
    hash_id: str
    online: int
    on_order: int


class DriversFatigue(BaseModel):
    timestamp: str
    drivers: List[DriverFatigue]


class Auth:
    x_authorization: str
    x_request_id: str
