from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional


class EndpointInfo(BaseModel):
    id: UUID
    endpoint: str


class EndpointsBody(BaseModel):
    identifiers: List[UUID]


class EndpointResponse(BaseModel):
    endpoints: List[EndpointInfo]


class DriverShares(BaseModel):
    hash_id: str
    shares: List[int]


class ControlBody(BaseModel):
    start: datetime
    end: Optional[datetime]
    drivers: List[DriverShares]
    chain: List[UUID]


class DriverFatigue(BaseModel):
    hash_id: str
    online: int
    on_order: int


class FatigueBody(BaseModel):
    timestamp: datetime
    drivers: List[DriverFatigue]


class SharesBody(BaseModel):
    next: Optional[UUID]
    drivers: List[DriverShares]
