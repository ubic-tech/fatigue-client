from pydantic import BaseModel


class StatusResponse(BaseModel):
    code: str
    message: str


ERROR = StatusResponse(code="503", message="NOT OK")
SUCCESS = StatusResponse(code="200", message="OK")
