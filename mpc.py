from random import randint, seed
from common.utils import *
from config import AggregatorConfig as AggrConf
from models.models import DriverData
from typing import List


def get_rand_pair(base: int) -> (int, int):
    seed(datetime.now().microsecond)
    f = randint(1000, 2000)
    s = base - f
    return (f, s) if randint(0, 1) else (s, f)


class OperationError(Exception):
    pass


def get_next_endpoint_hash_id(chain: List[str]) -> str:
    try:  # trying find 'myself' in the chain
        self_index = chain.index(AggrConf.AGGR_HASH_ID)  # get index of aggr in chain
    except ValueError:
        raise OperationError
    try:  # trying find next aggr in chain
        return chain[self_index + 1]
    except IndexError:  # means 'me' is the last aggregator in the chain
        return ""


async def common_strategy(headers, req_body, route, data_extractor):
    ts = timestamp_to_datetime(req_body.timestamp)

    drivers_hash_ids = []
    for _d in req_body.drivers:
        drivers_hash_ids.append(_d.hash_id)
    self_data = data_extractor(ts, drivers_hash_ids)  # Mapping[DriverID, Share]

    print(self_data)  # DBG

    if next_endpoint_hash_id := get_next_endpoint_hash_id(req_body.chain):
        #next_endpoint_url = await get_endpoint_url_by_hash(next_endpoint_hash_id)  # request in advance
        ubic_drivers_shares = []  # to be sent to UBIC
        for i, driver in enumerate(req_body.drivers):
            self_shares = self_data[driver.hash_id]
            ubic_driver_data = DriverData(hash_id=driver.hash_id, shares=[])  # to be appended to ubic_drivers_shares
            for j, share in enumerate(self_shares):
                for_ubic, for_common = get_rand_pair(int(share))  # for_ubic + for_common == d
                ubic_driver_data.shares.append(for_ubic)
                req_body.drivers[i].shares[j] += for_common  # add 'my' share summed up with common
            ubic_drivers_shares.append(ubic_driver_data)

        print("ubic_drivers_shares", ubic_drivers_shares, "\n\n")  # DBG
        print("req_body", req_body.drivers, "\n\n")  # DBG

        #r = await request(AggrConf.UBIC_URL + AggrConf.SHARES_ROUTE,
        #                  headers=headers,
        #                  json=ubic_drivers_shares)
        #if r is None:  # handle errors
        #    pass

        #r = await request(next_endpoint_url + route, headers=headers, json=req_body)
        #if r is None:  # handle errors
        #    # raise OperationError
        #    pass
    else:
        for i, driver_data in enumerate(req_body.drivers):  # sum up 'my' shares with received ones
            _id = driver_data.hash_id
            self_shares = self_data[_id]
            for j, share in enumerate(self_shares):  # common shares += "my" shares gotten by hash_id
                req_body.drivers[i].shares[j] += self_shares[j]
        # simply send ubic our share summed with total
        #r = request(AggrConf.UBIC_URL + AggrConf.SHARES_ROUTE, headers=headers, json=req_body)
        #if r is None:  # handle errors
        #    pass
        print("req_body", req_body.drivers, "\n\n")
