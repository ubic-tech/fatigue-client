from random import randint, seed
from common.utils import *
from config import AggregatorConfig as AggrConf
from models.models import DriverData


def get_rand_pair(base: int) -> (int, int):
    seed(datetime.now().microsecond)
    f = randint(1000, 2000)
    s = base - f
    return (f, s) if randint(0, 1) else (s, f)


class OperationError(Exception):
    pass


async def mpc_strategy(headers, req_body, route, aggregator, data_extractor):
    try:  # trying find 'myself' in the chain
        self_index = req_body.chain.index(aggregator.id)  # get index of aggr in chain
    except ValueError:
        raise OperationError

    ts = timestamp_to_datetime(req_body.timestamp)
    drivers_hash_ids = []
    for _d in req_body.drivers:
        drivers_hash_ids.append(_d["hash_id"])
    self_data = data_extractor(ts, drivers_hash_ids)  # Mapping[DriverID, Share]

    try:  # trying find next aggr in chain
        next_aggr_hash_id = req_body.chain[self_index + 1]
    except IndexError:  # means 'me' is the last aggregator in the chain
        for i, driver_data in enumerate(req_body.drivers):  # sum up 'my' shares with received ones
            _id = driver_data["hash_id"]
            req_body.drivers[i]["share"] += self_data[_id]  # common share + "my" shares gotten by hash_id
        # simply send ubic our share summed with total
        r = request(AggrConf.UBIC_URL + AggrConf.V1_SHARES,
                    headers=headers,
                    json=req_body)
        if r is None:  # handle errors
            pass
        return

    next_aggr_url = await get_endpoint_url_by_hash(next_aggr_hash_id)  # request in advance
    ubic_drivers_shares = []  # to be sent to UBIC
    for i, driver in enumerate(req_body.drivers):
        self_share = self_data[driver.hash_id]
        for_ubic, for_common = get_rand_pair(int(self_share))  # for_ubic + for_common == d

        ubic_driver_share = DriverData()  # to be appended to ubic_drivers_shares
        ubic_driver_share.hash_id = driver.hash_id
        ubic_driver_share.share = for_ubic
        ubic_drivers_shares.append(ubic_driver_share)

        req_body.drivers[i].share += for_common  # add 'my' share summed up with common

    r = await request(AggrConf.UBIC_URL + AggrConf.V1_SHARES,
                      headers=headers,
                      json=ubic_drivers_shares)
    if r is None:  # handle errors
        raise OperationError

    r = await request(next_aggr_url + route, headers=headers, json=req_body)
    if r is None:  # handle errors
        raise OperationError
