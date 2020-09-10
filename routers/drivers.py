from uuid import UUID

from fastapi import Header, APIRouter, Request
from cachetools.func import ttl_cache
from pydantic.error_wrappers import ValidationError

from utils.utils import request, OperationError
from models import drivers, common
from repository.clickhouse_repository import ClickhouseRepository
from core.mpc import continue_mpc, finalize_mpc
from config import AggregatorConfig as AggrConf

router = APIRouter()
db = ClickhouseRepository(AggrConf.CLICK_HOUSE_URL,
                          AggrConf.AGGR_NAME)


@ttl_cache(ttl=AggrConf.ENDPOINTS_TTL)
async def get_endpoint_by_uuid(uuid) -> str:
    route = AggrConf.UBIC_URL + AggrConf.ENDPOINTS_ROUTE
    resp = await request(route, json={"identifiers": [uuid, ]})
    try:
        return drivers.EndpointResponse(**resp).endpoints[0].endpoint
    except (ValidationError, IndexError):
        raise OperationError


def get_next_endpoint_uuid(chain: drivers.List[UUID], my_uuid: str) -> str:
    """
    Pops AggrConf.AGGR_HASH_ID from the chain
    the 1st hash ID is expected to be AggrConf.AGGR_UUID
        raises OperationError if not
    :param chain: list of endpoints' hash IDs
    :param my_uuid: this aggregator's hash ID
    :return: hash ID of an endpoint following after AggrConf.AGGR_UUID
        or an empty string if does not exist
    """
    try:  # the 1st uuid is expected to be 'mine' and should be popped out
        if str(chain.pop(0)) != my_uuid:
            raise OperationError
    except IndexError:
        raise OperationError
    try:  # try getting next aggr in chain
        return str(chain[0])  # return the next endpoint's uuid
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
    ts = req_body.timestamp
    drivers_hash_ids = [d.hash_id for d in req_body.drivers]
    my_data = data_extractor(drivers_hash_ids, ts, *data_extractor_params)
    next_endpoint_uuid = get_next_endpoint_uuid(req_body.chain,
                                                AggrConf.AGGR_UUID)
    if len(next_endpoint_uuid):
        # next_endpoint = await get_endpoint_by_uuid(next_endpoint_uuid)
        for_ubic, for_next_aggr = continue_mpc(req_body.drivers, my_data)
        # await request(next_endpoint+path, headers=headers, json=for_next_aggr)
        # await request(ubic_shares_route, headers=headers, json=for_ubic)
    else:
        for_ubic = finalize_mpc(req_body.drivers, my_data)
        # await request(ubic_shares_route, headers=headers, json=for_ubic)

    return common.SUCCESS


@router.post("/drivers/fatigue",
             response_model=common.StatusResponse,
             response_model_exclude_unset=True)
def fatigue(raw_request: Request,
            fatigue_drivers: drivers.FatigueBody):
    # handle fatigue_drivers here
    return common.SUCCESS


@router.post("/drivers/online/hourly",
             response_model=common.StatusResponse,
             response_model_exclude_unset=True)
async def online_hourly(raw_request: Request,
                        online_hourly_data: drivers.ControlBody,
                        x_request_id: str = Header(...)):
    return await process(x_request_id,
                         online_hourly_data,
                         raw_request.url.path,
                         db.get_hourly)


@router.post("/drivers/online/quarter_hourly",
             response_model=common.StatusResponse,
             response_model_exclude_unset=True)
async def online_quarter_hourly(raw_request: Request,
                                online_quarter_hourly_data: drivers.ControlBody,
                                x_request_id: str = Header(...)):
    return await process(x_request_id,
                         online_quarter_hourly_data,
                         raw_request.url.path,
                         db.get_quarter_hourly)


@router.post("/drivers/on_order",
             response_model=common.StatusResponse,
             response_model_exclude_unset=True)
async def on_order(raw_request: Request,
                   on_order_data: drivers.ControlBody,
                   x_request_id: str = Header(...)):
    return await process(x_request_id,
                         on_order_data,
                         raw_request.url.path,
                         db.get_on_order,
                         on_order_data.start)
