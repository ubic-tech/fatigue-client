from random import randint, seed
from common.utils import *
from config import AggregatorConfig as AggrConf
from models.models import DriverData
from typing import List, Mapping
from db.drivers_repository import DriverID, Share


def get_rand_pair(base: int) -> (int, int):
    seed(datetime.now().microsecond)
    f = randint(1000, 2000)
    s = base - f
    return (f, s) if randint(0, 1) else (s, f)


class OperationError(Exception):
    pass


def get_next_endpoint_hash_id(chain: List[str]) -> str:
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
                 self_db_data: Mapping[DriverID, List[Share]]) -> List[DriverData]:
    ubic_drivers_shares = []  # to be sent to UBIC
    for i, driver in enumerate(request_drivers):
        self_shares = self_db_data[driver.hash_id]
        ubic_driver_data = DriverData(hash_id=driver.hash_id, shares=[])  # to be appended to ubic_drivers_shares
        for j, share in enumerate(self_shares):
            for_ubic, for_common = get_rand_pair(int(share))  # for_ubic + for_common == share
            ubic_driver_data.shares.append(for_ubic)
            request_drivers[i].shares[j] += for_common  # add 'my' share summed up with common
        ubic_drivers_shares.append(ubic_driver_data)
    return ubic_drivers_shares


def finalize_mpc(request_drivers: List[DriverData],
                 self_db_data: Mapping[DriverID, List[Share]]):
    for i, driver_data in enumerate(request_drivers):  # sum up 'my' shares with received ones
        _id = driver_data.hash_id
        self_shares = self_db_data[_id]
        for j, share in enumerate(self_shares):  # common shares += "my" shares gotten by hash_id
            request_drivers[i].shares[j] += self_shares[j]


async def common_strategy(headers, req_body, route, data_extractor):
    ubic_shares_route = AggrConf.UBIC_URL + AggrConf.SHARES_ROUTE
    ts = timestamp_to_datetime(req_body.timestamp)

    #  todo: use list gen?
    drivers_hash_ids = []
    for _d in req_body.drivers:
        drivers_hash_ids.append(_d.hash_id)
    self_db_data = data_extractor(ts, drivers_hash_ids)  # Mapping[DriverID, Share]

    print("self_db_data: ", self_db_data)  # DBG

    if next_endpoint_hash_id := get_next_endpoint_hash_id(req_body.chain):
        #next_endpoint_url = await get_endpoint_url_by_hash(next_endpoint_hash_id)  # request in advance
        ubic_drivers_shares = continue_mpc(req_body.drivers, self_db_data)

        print("ubic_drivers_shares: ", ubic_drivers_shares)  # DBG
        print("forwarding req: ", req_body.drivers)  # DBG

        #await request(ubic_shares_route, headers=headers, json=ubic_drivers_shares)

        #await request(next_endpoint_url + route, headers=headers, json=req_body)
    else:
        finalize_mpc(req_body.drivers, self_db_data)
        # simply send ubic our share summed with total
        #await request(ubic_shares_route, headers=headers, json=req_body)
        print("forwarding req: ", req_body.drivers)
    print("\n\n")
