from random import randint, seed
from datetime import datetime
from utils import *
from models.models import DriverData
from aio_requests import post


def get_rand_pair(base: int) -> (int, int):
    seed(datetime.now().microsecond)
    f = randint(1000, 2000)
    s = base - f
    return (f, s) if randint(0, 1) else (s, f)


class Violation(Exception):
    pass


async def mpc_strategy(headers, request, route, aggregator, data_extractor):
    try:  # trying find 'myself' in the chain
        self_index = request.chain.index(aggregator.id)  # get index of aggr in chain
    except ValueError:
        raise Violation

    try:  # trying find next aggr in chain
        next_aggr_hash_id = request.chain[self_index + 1]
    except IndexError:  # means 'me' is the last aggregator in the chain
        for i, driver in enumerate(request.drivers):  # sum up 'my' shares with received ones
            driver_data = data_extractor(driver.hash_id, request.timestamp)
            for j, d in enumerate(driver_data):  # 1 or 4 values in list are expected
                request.drivers[i].shares[j] += d
        r = post(UBIC_URL + V1_SHARES, headers, data=dumps(request))  # simply send ubic our share summed with total
        if r is None:  # handle errors
            pass
        return SUCCESS

    ubic_drivers_shares = []  # to be sent to UBIC
    next_aggr_url = await get_endpoint_url_by_hash(next_aggr_hash_id,
                                                   headers["X-Authorization"])
    for i, driver in enumerate(request.drivers):
        ubic_driver_shares = DriverData()  # to be appended to ubic_drivers_shares
        ubic_driver_shares.hash_id = driver.hash_id
        raw_driver_data = data_extractor(driver.hash_id, request.timestamp)  # value from driversDB: [share, ...]
        for j, d in enumerate(raw_driver_data):
            for_ubic, for_common = get_rand_pair(int(d))  # for_ubic + for_common == d
            request.drivers[i].shares[j] += for_common  # add 'my' share summed up with common
            ubic_driver_shares.shares.append(for_ubic)  # keep all shares (looks like: [share,...]) of a driver
        ubic_drivers_shares.append(ubic_driver_shares)

    r = await post(UBIC_URL + V1_SHARES, headers, data=dumps(ubic_drivers_shares))
    if r is None:  # handle errors
        raise Violation

    r = await post(next_aggr_url + route, headers=headers, data=dumps(request))
    if r is None:  # handle errors
        raise Violation
    return SUCCESS
