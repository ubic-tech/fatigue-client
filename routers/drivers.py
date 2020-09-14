from uuid import UUID

from fastapi import Header, APIRouter, Request, BackgroundTasks
from pydantic.error_wrappers import ValidationError
from aiocache import cached
from typing import Iterable, List

from utils.utils import request, OperationError
from models import drivers, common
from repository.clickhouse_repository import ClickhouseRepository
from repository.drivers_repository import DriverID
from core.mpc import continue_mpc, finalize_mpc
from config import AggregatorConfig as AggrConf

router = APIRouter()
db = ClickhouseRepository(AggrConf.CLICK_HOUSE_URL,
                          AggrConf.AGGR_NAME)


@cached(ttl=AggrConf.ENDPOINTS_TTL)
async def get_endpoint_by_uuid(uuid) -> str:
    route = AggrConf.UBIC_URL + AggrConf.ENDPOINTS_ROUTE
    endpoints_request = drivers.EndpointsBody(identifiers=[UUID(uuid)])
    resp = await request(route, data=endpoints_request.json())
    try:
        return drivers.EndpointResponse(**resp).endpoints[0].endpoint
    except (ValidationError, IndexError):
        raise OperationError


def get_next_endpoint_uuid(chain: drivers.List[UUID], my_uuid: str):
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
        return None


async def process(x_request_id, req_body, path, my_data):
    """
    organizes strategy of MPC and web request forwarding
    :param x_request_id: header from request to be forwarded
    :param req_body: request's data body (JSON is expected)
    :param path: url specifying the MPC destination
    :param my_data: data extraction method appropriate for
        current MPC destination
    """
    headers = {"X-Request-Id": x_request_id, }
    r = common.ERROR
    shares_body = None

    while next_endpoint_uuid := get_next_endpoint_uuid(req_body.chain,
                                                       AggrConf.AGGR_UUID):
        next_endpoint = await get_endpoint_by_uuid(next_endpoint_uuid)
        for_ubic, for_next_aggr = continue_mpc(req_body.drivers, my_data)
        ctrl_body = drivers.ControlBody(start=req_body.start,
                                        end=req_body.end,
                                        chain=req_body.chain,
                                        drivers=for_next_aggr)
        r = await request(next_endpoint + path, headers=headers, data=ctrl_body.json())
        shares_body = drivers.SharesBody(next=UUID(next_endpoint_uuid), drivers=for_ubic)

    if not next_endpoint_uuid:
        r = common.SUCCESS
        for_ubic = finalize_mpc(req_body.drivers, my_data)
        shares_body = drivers.SharesBody(drivers=for_ubic)

    if r == common.SUCCESS:
        await request(AggrConf.UBIC_URL + AggrConf.SHARES_ROUTE,
                      headers=headers,
                      data=shares_body.json())

    return common.SUCCESS


def get_hash_ids(drivers_shares: List[drivers.DriverShares]
                 ) -> Iterable[DriverID]:
    return [d.hash_id for d in drivers_shares]


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
                        ctrl_body: drivers.ControlBody,
                        background_tasks: BackgroundTasks,
                        x_request_id: str = Header(...)):
    background_tasks.add_task(process,
                              x_request_id,
                              ctrl_body,
                              raw_request.url.path,
                              db.get_hourly(
                                  get_hash_ids(ctrl_body.drivers),
                                  ctrl_body.start)
                              )
    return common.SUCCESS


@router.post("/drivers/online/history_hourly",
             response_model=common.StatusResponse,
             response_model_exclude_unset=True)
async def history_hourly(raw_request: Request,
                         ctrl_body: drivers.ControlBody,
                         background_tasks: BackgroundTasks,
                         x_request_id: str = Header(...)):
    background_tasks.add_task(process,
                              x_request_id,
                              ctrl_body,
                              raw_request.url.path,
                              db.get_history_hourly(
                                  get_hash_ids(ctrl_body.drivers),
                                  ctrl_body.start)
                              )
    return common.SUCCESS


@router.post("/drivers/online/quarter_hourly",
             response_model=common.StatusResponse,
             response_model_exclude_unset=True)
async def online_quarter_hourly(raw_request: Request,
                                ctrl_body: drivers.ControlBody,
                                background_tasks: BackgroundTasks,
                                x_request_id: str = Header(...)):
    background_tasks.add_task(process,
                              x_request_id,
                              ctrl_body,
                              raw_request.url.path,
                              db.get_quarter_hourly(
                                  get_hash_ids(ctrl_body.drivers),
                                  ctrl_body.start)
                              )
    return common.SUCCESS


@router.post("/drivers/on_order",
             response_model=common.StatusResponse,
             response_model_exclude_unset=True)
async def on_order(raw_request: Request,
                   ctrl_body: drivers.ControlBody,
                   background_tasks: BackgroundTasks,
                   x_request_id: str = Header(...)):
    background_tasks.add_task(process,
                              x_request_id,
                              ctrl_body,
                              raw_request.url.path,
                              db.get_on_order(
                                  get_hash_ids(ctrl_body.drivers),
                                  ctrl_body.start,
                                  ctrl_body.end)
                              )
    return common.SUCCESS
