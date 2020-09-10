from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional


class EndpointInfo(BaseModel):
    id: str
    endpoint: str


class EndpointResponse(BaseModel):
    endpoints: List[EndpointInfo]


class DriverShares(BaseModel):
    hash_id: str
    shares: List[int]


class ControlBody(BaseModel):
    timestamp: datetime
    start: Optional[datetime]
    chain: List[UUID]
    drivers: List[DriverShares]


class DriverFatigue(BaseModel):
    hash_id: str
    online: int
    on_order: int


class FatigueBody(BaseModel):
    timestamp: datetime
    drivers: List[DriverFatigue]
