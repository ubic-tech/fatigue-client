from fastapi import Header, APIRouter, Request
from models.drivers import *
from repository.clickhouse_repository import ClickhouseRepository
from mpc.mpc import compute
from config import AggregatorConfig as AggrConf
from utils.utils import timestamp_to_datetime, request, OperationError

ERROR = {'code': "503", 'message': "NOT OK"}
SUCCESS = {'code': "200", 'message': "OK"}
router = APIRouter()
db = ClickhouseRepository(AggrConf.CLICK_HOUSE_URL,
                          AggrConf.AGGR_NAME)

PREFIX_URL = "/v1"


# cacheble
async def get_endpoint_url_by_hash(hash_id) -> str:
    route = AggrConf.UBIC_URL + AggrConf.ENDPOINTS_ROUTE
    resp = await request(route, json={"identifiers": [hash_id, ]})
    resp = {'data': 'anything'}
    if resp is None:
        pass  # todo: validate
    return EndpointResponse(**resp).endpoints[0].endpoint


def get_next_endpoint_hash_id(chain: List[str], my_hash_id: str) -> str:
    """
    Pops AggrConf.AGGR_HASH_ID from the chain
    the 1st hash ID is expected to be AggrConf.AGGR_HASH_ID
        raises OperationError if not
    :param chain: list of endpoints' hash IDs
    :param my_hash_id: this aggregator's hash ID
    :return: hash ID of an endpoint following after AggrConf.AGGR_HASH_ID
        or an empty string if does not exist
    """
    try:  # the 1st hash_id is expected to be 'mine'
        if chain[0] != my_hash_id:
            raise OperationError
    except IndexError:
        raise OperationError
    chain.pop(0)  # pop 'my' hash_id
    try:  # try getting next aggr in chain
        return chain[0]  # return the next endpoint's hash_id
    except IndexError:  # means 'I' am the last aggregator in the chain
        return ""


async def process(x_request_id, req_body, path, data_extractor,
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

    for_ubic, req_body.drivers = compute(req_body.drivers, my_db_data, next_endpoint_hash_id)

    print("\n\n")
    return SUCCESS
    if next_endpoint_hash_id:
        await request(next_endpoint_url + path, headers=headers, json=req_body)
        await request(ubic_shares_route, headers=headers, json=for_ubic)
    else:
        req_body.drivers = for_ubic
        await request(ubic_shares_route, headers=headers, json=req_body)

    return SUCCESS


@router.get("/health",
            response_model=ServerResponse,
            response_model_exclude_unset=True)
def health():
    """simple heartbeat"""
    return SUCCESS


@router.post("/drivers/fatigue",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
def fatigue(raw_request: Request,
            drivers: DriversFatigue):
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
    print(raw_request.headers)  # DBG
    print(raw_request.url.path)  # DBG
    print(drivers)  # DBG
    return SUCCESS


@router.post("/drivers/online/hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def online_hourly(raw_request: Request,
                        online_hourly_data: OnlineHourly,
                        x_request_id: str = Header(...)):
    return await process(x_request_id,
                         online_hourly_data,
                         raw_request.url.path,
                         db.get_hourly)


@router.post("/drivers/online/quarter_hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def online_quarter_hourly(raw_request: Request,
                                online_quarter_hourly_data: OnlineQuarterHourly,
                                x_request_id: str = Header(...)):
    return await process(x_request_id,
                         online_quarter_hourly_data,
                         raw_request.url.path,
                         db.get_quarter_hourly)


@router.post("/drivers/on_order",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
async def on_order(raw_request: Request,
                   on_order_data: OnOrder,
                   x_request_id: str = Header(...)):
    return await process(x_request_id,
                         on_order_data,
                         raw_request.url.path,
                         db.get_on_order,
                         timestamp_to_datetime(on_order_data.start))
