from pydantic import BaseModel
from uuid import UUID
from typing import List


class EndpointInfo(BaseModel):
    id: UUID
    endpoint: str


class EndpointsBody(BaseModel):
    identifiers: List[UUID]


class EndpointResponse(BaseModel):
    endpoints: List[EndpointInfo]


class StatusResponse(BaseModel):
    code: str
    message: str


ERROR = StatusResponse(code="503", message="NOT OK")
SUCCESS = StatusResponse(code="200", message="OK")
