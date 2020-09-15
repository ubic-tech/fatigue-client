from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional


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
