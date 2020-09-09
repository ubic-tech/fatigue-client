from fastapi import APIRouter
from models.common import StatusResponse, SUCCESS

router = APIRouter()


@router.get("/health",
            response_model=StatusResponse,
            response_model_exclude_unset=True)
def health():
    """simple heartbeat"""
    return SUCCESS
