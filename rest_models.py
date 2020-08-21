from pydantic import BaseModel
from typing import List


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
