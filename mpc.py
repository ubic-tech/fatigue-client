from random import randint, seed
from datetime import datetime
from utils import *
from rest_models import DriverData


def get_rand_pair(base: int) -> (int, int):
    seed(datetime.now().microsecond)
    f = randint(1000, 2000)
    s = base - f
    return (f, s) if randint(0, 1) else (s, f)


def mpc_strategy(headers, request, route, aggregator, data_extractor):
    try:
        self_index = request.chain.index(aggregator.id)  # get index of aggr in chain
    except ValueError:
        return ERROR

    try:
        next_aggr_hash_id = request.chain[self_index + 1]
        next_aggr_url = get_endpoint_url_by_hash(next_aggr_hash_id,
                                                 headers["X-Authorization"])
    except IndexError:  # means this is the last aggregator in the chain
        for i, driver in enumerate(request.drivers):
            driver_data = data_extractor(driver.hash_id, request.timestamp)
            for j, d in enumerate(driver_data):
                request.drivers[i].shares[j] += d
        r = send(UBIC_URL + V1_SHARES, headers, data=dumps(request))  # simply send ubic our share summed with total
        if r is None:
            pass
        return SUCCESS

    ubic_shares = []
    for i, driver in enumerate(request.drivers):
        ubic_part = DriverData()
        ubic_part.hash_id = driver.hash_id
        raw_driver_data = data_extractor(driver.hash_id, request.timestamp)
        for j, d in enumerate(raw_driver_data):
            for_ubic, for_common = get_rand_pair(int(d))
            request.drivers[i].shares[j] += for_common
            ubic_part.shares.append(for_ubic)
        ubic_shares.append(ubic_part)

    r = send(UBIC_URL + V1_SHARES, headers, data=dumps(ubic_shares))
    if r is None:  # handle errors
        return ERROR

    r = send(next_aggr_url + route, headers=headers, data=dumps(request))
    if r is None:  # handle errors
        return ERROR
    return SUCCESS
