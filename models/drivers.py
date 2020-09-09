from pydantic import BaseModel
from typing import List


class EndpointInfo(BaseModel):
    id: str
    endpoint: str


class EndpointResponse(BaseModel):
    endpoints: List[EndpointInfo]


class DriverShares(BaseModel):
    hash_id: str
    shares: List[int]


class ControlBody(BaseModel):
    timestamp: str
    chain: List[str]
    drivers: List[DriverShares]


class OnOrder(ControlBody):
    start: str


class DriverFatigue(BaseModel):
    hash_id: str
    online: int
    on_order: int


class FatigueBody(BaseModel):
    timestamp: str
    drivers: List[DriverFatigue]
