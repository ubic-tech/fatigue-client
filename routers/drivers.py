from fastapi import Header, APIRouter
from models.models import *
from repository.clickhouse_repository import ClickhouseRepository
from mpc.mpc import compute
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


async def common_strategy(headers, req_body, route, data_extractor,
                          *data_extractor_params):
    """
        organizes strategy of MPC and web request forwarding
        :param headers: headers from request to be forwarded
        :param req_body: request's data body (JSON is expected)
        :param route: url specifying the MPC destination
        :param data_extractor: data extraction method appropriate for
            current MPC destination
        """
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

    for_ubic, req_body.drivers = compute(req_body.drivers, my_db_data, next_endpoint_hash_id)

    print("\n\n")
    return
    if next_endpoint_hash_id:
        await request(next_endpoint_url + route, headers=headers, json=req_body)
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
def fatigue(request: DriversFatigue):
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
        эмулировать блокировку как-то так: my.drivers[hash_id].block()?
        """
    print(request)  # DBG
    return SUCCESS


@router.post("/drivers/online/hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def online_hourly(request: OnlineHourly,
                        x_request_id: str = Header(...)):
    data_extractor = db.get_hourly
    route = PREFIX_URL + "/drivers/online/hourly"

    headers = {"X-Request-Id": x_request_id, }
    await common_strategy(headers,
                          request,
                          route,
                          data_extractor)
    return SUCCESS


# headers to single param
# routing from request
@router.post("/drivers/online/quarter_hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def online_quarter_hourly(request: OnlineQuarterHourly,
                                x_request_id: str = Header(...)):
    data_extractor = db.get_quarter_hourly
    route = PREFIX_URL + "/drivers/online/quarter_hourly"
    headers = {"X-Request-Id": x_request_id, }
    await common_strategy(headers, request, route, data_extractor)
    print(request)  # DBG
    return SUCCESS


@router.post("/drivers/on_order",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def on_order(request: OnOrder,
                   x_request_id: str = Header(...)):
    start = timestamp_to_datetime(request.start)
    data_extractor = db.get_on_order
    route = PREFIX_URL + "/drivers/on_order"
    headers = {"X-Request-Id": x_request_id, }
    await common_strategy(headers, request, route, data_extractor, start)
    print(request)  # DBG
    return SUCCESS
