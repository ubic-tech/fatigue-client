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
db = ClickhouseRepository(AggrConf.CLICK_HOUSE_URL, AggrConf.AGGR_NAME)


@cached(ttl=AggrConf.ENDPOINTS_TTL)
async def get_endpoint_by_uuid(uuid: UUID) -> str:
    route = AggrConf.UBIC_URL + AggrConf.ENDPOINTS_ROUTE
    endpoints_request = drivers.EndpointsBody(identifiers=[uuid, ])
    resp = await request(route, data=endpoints_request.json())
    try:
        return drivers.EndpointResponse(**resp).endpoints[0].endpoint
    except (ValidationError, IndexError):
        raise OperationError


def check_if_mine_uuid_1st_and_pop(chain: drivers.List[UUID], mine: UUID):
    try:
        assert chain.pop(0) == mine
    except (IndexError, AssertionError):
        raise OperationError


def get_next_endpoint_uuid(chain: drivers.List[UUID]):
    try:
        return chain[0]
    except IndexError:
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
    # if no next endpoint simply send 'my' data += ctrl_body's to Ubic
    if not (next_endpoint_uuid := get_next_endpoint_uuid(req_body.chain)):
        for_ubic = finalize_mpc(req_body.drivers, my_data)
        shares_body = drivers.SharesBody(drivers=for_ubic)
        await request(AggrConf.UBIC_URL + AggrConf.SHARES_ROUTE,
                      headers=headers,
                      data=shares_body.json())
        return

    # if 'I' am not the last 'I' should continue MPC
    for_ubic, for_next_aggr = continue_mpc(req_body.drivers, my_data)
    ctrl_body = drivers.ControlBody(start=req_body.start,
                                    end=req_body.end,
                                    chain=req_body.chain,
                                    drivers=for_next_aggr)
    while next_endpoint_uuid:
        # keep trying to get a response from any of next endpoints
        next_endpoint = await get_endpoint_by_uuid(next_endpoint_uuid)
        r = await request(next_endpoint + path, headers=headers, data=ctrl_body.json())
        if common.StatusResponse(**r) != common.SUCCESS:
            req_body.chain.pop(0)  # pop unavailable endpoint
            next_endpoint_uuid = get_next_endpoint_uuid(req_body.chain)
            continue

        #  if next responded ok I can send my shares to Ubic and that is it for me
        shares_body = drivers.SharesBody(next=next_endpoint_uuid, drivers=for_ubic)
        await request(AggrConf.UBIC_URL + AggrConf.SHARES_ROUTE,
                      headers=headers,
                      data=shares_body.json())
        return


def get_hash_ids(drivers_shares: List[drivers.DriverShares]
                 ) -> Iterable[DriverID]:
    return [d.hash_id for d in drivers_shares]


@router.post("/drivers/fatigue",
             response_model=common.StatusResponse,
             response_model_exclude_unset=True)
def fatigue(_: Request, __: drivers.FatigueBody):
    # handle fatigue_drivers here
    return common.SUCCESS


@router.post("/drivers/online/hourly",
             response_model=common.StatusResponse,
             response_model_exclude_unset=True)
async def online_hourly(raw_request: Request,
                        ctrl_body: drivers.ControlBody,
                        background_tasks: BackgroundTasks,
                        x_request_id: str = Header(...)):
    check_if_mine_uuid_1st_and_pop(ctrl_body.chain, UUID(AggrConf.AGGR_UUID))
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
    check_if_mine_uuid_1st_and_pop(ctrl_body.chain, UUID(AggrConf.AGGR_UUID))
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
    check_if_mine_uuid_1st_and_pop(ctrl_body.chain, UUID(AggrConf.AGGR_UUID))
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
    check_if_mine_uuid_1st_and_pop(ctrl_body.chain, UUID(AggrConf.AGGR_UUID))
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
