from sys import maxsize
from copy import deepcopy
from random import randint

from typing import List, Mapping

from repository.drivers_repository import DriverID, Share
from models.drivers import DriverShares


def get_rand_pair(base: int) -> (int, int):
    """
    return a pair of random integers so that their sum == base
    :param base: integer to be splitted into 2 components
    :return: a pair of base's components
    """
    f = randint(-maxsize, maxsize)
    s = base - f
    return (f, s) if randint(0, 1) else (s, f)


def continue_mpc(request_drivers: List[DriverShares],
                 my_db_data: Mapping[DriverID, List[Share]]) \
        -> (List[DriverShares], List[DriverShares]):
    """
     adds one random number to each of request's shares and
        one for each hash_id pushes into a returned list
    :param request_drivers: drivers field from request body
    :param my_db_data: drivers data extracted with a certain DriverRepository's method
    :return: 2 lists of DriverShares with randomly generated shares
        one to be handled by Ubic the other to be handled by the next Endpoint
    """
    ubic_drivers_shares = []  # to be sent to UBIC
    driver_shares = deepcopy(request_drivers)
    for i, driver in enumerate(driver_shares):
        my_shares = my_db_data[driver.hash_id]
        ubic_driver_data = DriverShares(hash_id=driver.hash_id, shares=[])  # to be appended to ubic_drivers_shares
        for j, share in enumerate(my_shares):
            for_ubic, for_common = get_rand_pair(int(share))  # for_ubic + for_common == share
            ubic_driver_data.shares.append(for_ubic)
            driver_shares[i].shares[j] += for_common  # add 'my' share summed up with common
        ubic_drivers_shares.append(ubic_driver_data)
    return ubic_drivers_shares, driver_shares


def finalize_mpc(request_drivers: List[DriverShares],
                 my_db_data: Mapping[DriverID, List[Share]]) \
        -> List[DriverShares]:
    """
    adds my_db_data's shares to request_drivers' shares for each hash_id
    :param request_drivers: drivers field from request body
    :param my_db_data: drivers data extracted with
        a certain DriverRepository's method
    :return list of DriverShares objects so that for each hash ID
        each share from request_drivers summed with those from my_db_data
    """
    res = deepcopy(request_drivers)
    for i, driver_data in enumerate(res):  # sum up 'my' shares with received ones
        _id = driver_data.hash_id
        my_shares = my_db_data[_id]
        for j, share in enumerate(my_shares):  # common shares += "my" shares gotten by hash_id
            res[i].shares[j] += my_shares[j]
    return res


def compute(req_body_drivers: List[DriverShares],
            my_db_data: Mapping[DriverID, List[Share]],
            next_endpoint_hash_id: str) -> (List[DriverShares], List[DriverShares]):
    """
    if next_endpoint_hash_id is empty returns finalize_mpc()
        else returns continue_mpc()
    :param req_body_drivers: drivers field from request body
    :param my_db_data: drivers data extracted with a certain DriverRepository's method
    :param next_endpoint_hash_id: hash ID of an endpoint to forward MPC to
    :return: a pair of DriverShares objects lists containing shares
        to continue or finalize MPC
    """
    print("my_db_data: ", my_db_data)  # DBG

    if len(next_endpoint_hash_id):
        u, c = continue_mpc(req_body_drivers, my_db_data)  # DBG
        print("ubic_drivers_shares: ", u)  # DBG
        print("forwarding req: ", c)  # DBG
        return continue_mpc(req_body_drivers, my_db_data)
    else:
        u = finalize_mpc(req_body_drivers, my_db_data)  # DBG
        # simply our share summed with total
        print("forwarding req: ", u)
        return finalize_mpc(req_body_drivers, my_db_data), []
