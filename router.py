from fastapi import Header, APIRouter
from models.models import *
from db.clickhouse_repository import ClickhouseRepository
from aggregator import Aggregator
from core import common_strategy
from config import AggregatorConfig
from common.utils import timestamp_to_datetime

ERROR = {'code': "503", 'message': "NOT OK"}
SUCCESS = {'code': "200", 'message': "OK"}
router = APIRouter()
aggregator = Aggregator(AggregatorConfig.AGGR_HASH_ID,
                        ClickhouseRepository(AggregatorConfig.CLICK_HOUSE_URL,
                                             AggregatorConfig.AGGR_NAME))

PREFIX_URL = "/v1"


@router.get("/health",
            response_model=ServerResponse,
            response_model_exclude_unset=True)
def health():
    """simple heartbeat"""
    return SUCCESS


@router.post("/drivers/fatigue",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
def drivers_fatigue(request: DriversFatigue):
    """X-Authorization and X-Request-Id required
        stores data of tired drivers
        и что с этим делать?
        допустим пришло:
        {
            "timestamp": "2020-08-11T16:30:25.199",
            "drivers" : [
                {
                    "hash_id": "8xx8",
                    "online": "40",
                    "on_order": "20",
                },
                {
                    "hash_id": "8x7x8",
                    "online": "80",
                    "on_order": "20",
                },
            ]
        }
        какую реакцию запрогить?
        эмулировать блокировку как-то так: self.drivers[hash_id].block()?
        """
    print(request)  # DBG
    return SUCCESS


@router.post("/drivers/online/hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def drivers_online_hourly(request: OnlineHourly,
                                x_request_id: str = Header(...)):
    data_extractor = aggregator.drivers_db.get_hourly
    route = PREFIX_URL + "/drivers/online/hourly"

    headers = {"X-Request-Id": x_request_id, }
    await common_strategy(headers, request, route, data_extractor)
    return SUCCESS


@router.post("/drivers/online/quarter_hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def drivers_online_quarter_hourly(request: OnlineQuarterHourly,
                                        x_request_id: str = Header(...)):
    data_extractor = aggregator.drivers_db.get_quarter_hourly
    route = PREFIX_URL + "/drivers/online/quarter_hourly"
    headers = {"X-Request-Id": x_request_id, }
    await common_strategy(headers, request, route, data_extractor)
    print(request)  # DBG
    return SUCCESS


@router.post("/drivers/on_order",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def drivers_on_order(request: OnOrder,
                           x_request_id: str = Header(...)):
    start = timestamp_to_datetime(request.start)
    data_extractor = aggregator.drivers_db.get_on_order
    route = PREFIX_URL + "/drivers/on_order"
    headers = {"X-Request-Id": x_request_id, }
    await common_strategy(headers, request, route, data_extractor, start)
    print(request)  # DBG
    return SUCCESS
