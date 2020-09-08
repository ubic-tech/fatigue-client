from fastapi import Header, APIRouter, Request
from models.models import *
from repository.clickhouse_repository import ClickhouseRepository
from mpc.mpc import mpc
from config import AggregatorConfig as AggrConf
from common.utils import (
    timestamp_to_datetime,
    get_next_endpoint_hash_id,
    get_endpoint_url_by_hash,
)

ERROR = {'code': "503", 'message': "NOT OK"}
SUCCESS = {'code': "200", 'message': "OK"}
router = APIRouter()
db = ClickhouseRepository(AggrConf.CLICK_HOUSE_URL,
                          AggrConf.AGGR_NAME)

PREFIX_URL = "/v1"


async def compute(x_request_id, req_body, path, data_extractor,
                  *data_extractor_params):
    """
        organizes strategy of MPC and web request forwarding
        :param x_request_id: header from request to be forwarded
        :param req_body: request's data body (JSON is expected)
        :param path: url specifying the MPC destination
        :param data_extractor: data extraction method appropriate for
            current MPC destination
        """
    headers = {"X-Request-Id": x_request_id, }
    ubic_shares_route = AggrConf.UBIC_URL + AggrConf.SHARES_ROUTE
    ts = timestamp_to_datetime(req_body.timestamp)

    drivers_hash_ids = [d.hash_id for d in req_body.drivers]
    my_db_data = data_extractor(drivers_hash_ids, ts, *data_extractor_params)  # Mapping[DriverID, Share]
    if next_endpoint_hash_id := get_next_endpoint_hash_id(req_body.chain,
                                                          AggrConf.AGGR_HASH_ID):
        # next_endpoint_url = await get_endpoint_url_by_hash(next_endpoint_hash_id)  # request in advance
        pass
    else:
        next_endpoint_url = ""  # to eliminate warning

    for_ubic, req_body.drivers = mpc(req_body.drivers, my_db_data, next_endpoint_hash_id)

    print("\n\n")
    return
    if next_endpoint_hash_id:
        await request(next_endpoint_url + path, headers=headers, json=req_body)
        await request(ubic_shares_route, headers=headers, json=for_ubic)
    else:
        req_body.drivers = for_ubic
        await request(ubic_shares_route, headers=headers, json=req_body)


@router.get("/health",
            response_model=ServerResponse,
            response_model_exclude_unset=True)
def health():
    """simple heartbeat"""
    return SUCCESS


@router.post("/drivers/fatigue",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
def fatigue(drivers: DriversFatigue,
            request: Request):
    """X-Request-Id required
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
        эмулировать блокировку как-то так: my.drivers[hash_id].block()?
        """
    print(request.headers)  # DBG
    print(request.url.path)
    print(drivers)
    return SUCCESS


@router.post("/drivers/online/hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def online_hourly(online_hourly_data: OnlineHourly,
                        request: Request,
                        x_request_id: str = Header(...)):
    await compute(x_request_id,
                  online_hourly_data,
                  request.url.path,
                  db.get_hourly)
    return SUCCESS


@router.post("/drivers/online/quarter_hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def online_quarter_hourly(online_quarter_hourly_data: OnlineQuarterHourly,
                                request: Request,
                                x_request_id: str = Header(...)):
    await compute(x_request_id,
                  online_quarter_hourly_data,
                  request.url.path,
                  db.get_quarter_hourly)
    print(online_quarter_hourly_data)  # DBG
    return SUCCESS


@router.post("/drivers/on_order",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def on_order(on_order_data: OnOrder,
                   request: Request,
                   x_request_id: str = Header(...)):
    await compute(x_request_id,
                  on_order_data,
                  request.url.path,
                  db.get_on_order,
                  timestamp_to_datetime(on_order_data.start))
    print(request)  # DBG
    return SUCCESS
