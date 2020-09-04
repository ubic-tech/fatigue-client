from random import randint, seed
from common.utils import *
from config import AggregatorConfig as AggrConf
from models.models import DriverData
from typing import List, Mapping
from db.drivers_repository import DriverID, Share
from copy import deepcopy


def get_rand_pair(base: int) -> (int, int):
    """
    return a pair of random integers so that their sum == base
    :param base: integer to be splitted into 2 components
    :return: a pair of base's components
    """
    seed(datetime.now().microsecond)
    f = randint(1000, 2000)
    s = base - f
    return (f, s) if randint(0, 1) else (s, f)


class OperationError(Exception):
    pass


def get_next_endpoint_hash_id(chain: List[str]) -> str:
    """
    Pops AggrConf.AGGR_HASH_ID from the chain
    the 1st hash ID is expected to be AggrConf.AGGR_HASH_ID
        raises OperationError if not
    :param chain: list of endpoints' hash IDs
    :return: hash ID of an endpoint following after AggrConf.AGGR_HASH_ID
        or an empty string if does not exist
    """
    try:  # the 1st hash_id is expected to be 'mine'
        if chain[0] != AggrConf.AGGR_HASH_ID:
            raise OperationError
    except IndexError:
        raise OperationError
    chain.pop(0)  # pop 'my' hash_id
    try:  # try getting next aggr in chain
        return chain[0]  # return the next endpoint's hash_id
    except IndexError:  # means 'I' am the last aggregator in the chain
        return ""


def continue_mpc(request_drivers: List[DriverData],
                 self_db_data: Mapping[DriverID, List[Share]])\
        -> (List[DriverData], List[DriverData]):
    """
     adds one random number to each of request's shares and
        one for each hash_id pushes into a returned list
    :param request_drivers: drivers field from request body
    :param self_db_data: drivers data extracted with a certain DriverRepository's method
    :return: 2 lists of DriverData with randomly generated shares
        one to be handled by Ubic the other to be handled by the next Endpoint
    """
    ubic_drivers_shares = []  # to be sent to UBIC
    common_driver_shares = deepcopy(request_drivers)
    for i, driver in enumerate(common_driver_shares):
        self_shares = self_db_data[driver.hash_id]
        ubic_driver_data = DriverData(hash_id=driver.hash_id, shares=[])  # to be appended to ubic_drivers_shares
        for j, share in enumerate(self_shares):
            for_ubic, for_common = get_rand_pair(int(share))  # for_ubic + for_common == share
            ubic_driver_data.shares.append(for_ubic)
            common_driver_shares[i].shares[j] += for_common  # add 'my' share summed up with common
        ubic_drivers_shares.append(ubic_driver_data)
    return ubic_drivers_shares, common_driver_shares


def finalize_mpc(request_drivers: List[DriverData],
                 self_db_data: Mapping[DriverID, List[Share]])\
        -> List[DriverData]:
    """
    adds self_db_data's shares to request_drivers' shares for each hash_id
    :param request_drivers: drivers field from request body
    :param self_db_data: drivers data extracted with
        a certain DriverRepository's method
    :return list of DriverData objects so that for each hash ID
        each share from request_drivers summed with those from self_db_data
    """
    res = deepcopy(request_drivers)
    for i, driver_data in enumerate(res):  # sum up 'my' shares with received ones
        _id = driver_data.hash_id
        self_shares = self_db_data[_id]
        for j, share in enumerate(self_shares):  # common shares += "my" shares gotten by hash_id
            res[i].shares[j] += self_shares[j]
    return res


def mpc_strategy(req_body_drivers: List[DriverData],
                 self_db_data: Mapping[DriverID, List[Share]],
                 next_endpoint_hash_id: str)\
        -> (List[DriverData], List[DriverData]):
    """
    if next_endpoint_hash_id is empty returns finalize_mpc()
        else returns continue_mpc()
    :param req_body_drivers: drivers field from request body
    :param self_db_data: drivers data extracted with a certain DriverRepository's method
    :param next_endpoint_hash_id: hash ID of an endpoint to forward MPC to
    :return: a pair of DriverData objects lists containing shares
        to continue or finalize MPC
    """
    print("self_db_data: ", self_db_data)  # DBG

    if len(next_endpoint_hash_id):
        u, c = continue_mpc(req_body_drivers, self_db_data)  # DBG
        print("ubic_drivers_shares: ", u)  # DBG
        print("forwarding req: ", c)  # DBG
        return continue_mpc(req_body_drivers, self_db_data)
    else:
        u = finalize_mpc(req_body_drivers, self_db_data)  # DBG
        # simply our share summed with total
        print("forwarding req: ", u)
        return finalize_mpc(req_body_drivers, self_db_data), []


async def common_strategy(headers, req_body, route, data_extractor, *data_extractor_params):
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
    self_db_data = data_extractor(ts, drivers_hash_ids, *data_extractor_params)  # Mapping[DriverID, Share]
    if next_endpoint_hash_id := get_next_endpoint_hash_id(req_body.chain):
        #next_endpoint_url = await get_endpoint_url_by_hash(next_endpoint_hash_id)  # request in advance
        pass
    else:
        next_endpoint_url = ""  # to eliminate warning

    for_ubic, req_body.drivers = mpc_strategy(req_body.drivers, self_db_data, next_endpoint_hash_id)

    print("\n\n")
    return
    if next_endpoint_hash_id:
        await request(next_endpoint_url + route, headers=headers, json=req_body)
        await request(ubic_shares_route, headers=headers, json=for_ubic)
    else:
        req_body.drivers = for_ubic
        await request(ubic_shares_route, headers=headers, json=req_body)
