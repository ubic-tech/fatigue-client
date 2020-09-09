from sys import maxsize
from copy import deepcopy
from random import randint

from typing import List, Mapping

from repository.drivers_repository import DriverID, Share
from models.drivers import DriverShares
# comments up

def get_rand_pair(base: int) -> (int, int):
    """
    return a pair of random integers so that their sum == base
    :param base: integer to be splitted into 2 components
    :return: a pair of base's components
    """
    f = randint(-maxsize, maxsize)
    s = base - f
    return (f, s) if randint(0, 1) else (s, f)


def continue_mpc(
        drivers: List[DriverShares],
        my_data: Mapping[DriverID, List[Share]]
) -> (List[DriverShares], List[DriverShares]):
    """
     adds one random number to each of request's shares and
        one for each hash_id pushes into a returned list
    :param drivers: drivers field from request body
    :param my_data: drivers data extracted with a certain DriverRepository's method
    :return: 2 lists of DriverShares with randomly generated shares
        one to be handled by Ubic the other to be handled by the next Endpoint
    todo: use numpy
    """
    ubic_drivers_shares = []
    next_aggr_drivers_shares = []
    for i, driver in enumerate(drivers):
        my_shares = my_data[driver.hash_id]  # no miss guarantee by caller
        ubic_driver_data = DriverShares(hash_id=driver.hash_id, shares=[])
        next_aggr_driver_data = DriverShares(hash_id=driver.hash_id, shares=[])
        for j, share in enumerate(my_shares):
            for_ubic, for_next_aggr = get_rand_pair(int(share))
            ubic_driver_data.shares.append(for_ubic)
            next_aggr_driver_data.shares.append(drivers[i].shares[j] + for_next_aggr)
        ubic_drivers_shares.append(ubic_driver_data)
        next_aggr_drivers_shares.append(next_aggr_driver_data)
    return ubic_drivers_shares, next_aggr_drivers_shares


def finalize_mpc(
        drivers: List[DriverShares],
        my_data: Mapping[DriverID, List[Share]]
) -> List[DriverShares]:
    """
    adds my_data's shares to request_drivers' shares for each hash_id
    :param drivers: drivers field from request body
    :param my_data: drivers data extracted with
        a certain DriverRepository's method
    :return list of DriverShares objects so that for each hash ID
        each share from request_drivers summed with those from my_data
    """
    ubic_drivers_shares = []
    for i, driver in enumerate(drivers):  # sum up 'my' shares with received ones
        ubic_driver_data = DriverShares(hash_id=driver.hash_id, shares=[])
        my_shares = my_data[driver.hash_id]
        for j, share in enumerate(my_shares):  # shares += "my" shares gotten by hash_id
            ubic_driver_data.shares.append(driver.shares[j] + my_shares[j])
        ubic_drivers_shares.append(ubic_driver_data)
    return ubic_drivers_shares


def compute(drivers: List[DriverShares],
            my_data: Mapping[DriverID, List[Share]],
            next_aggr_hash_id: str) -> (List[DriverShares], List[DriverShares]):
    """
    if next_endpoint_hash_id is empty returns finalize_mpc()
        else returns continue_mpc()
    :param drivers: drivers field from request body
    :param my_data: drivers data extracted with a certain DriverRepository's method
    :param next_aggr_hash_id: hash ID of an endpoint to forward MPC to
    :return: a pair of DriverShares objects lists containing shares
        to continue or finalize MPC
    """
    print("my_data: ", my_data)  # DBG

    if len(next_aggr_hash_id):
        u, c = continue_mpc(drivers, my_data)  # DBG
        print("ubic_drivers_shares: ", u)  # DBG
        print("forwarding req: ", c)  # DBG
        return continue_mpc(drivers, my_data)
    else:
        u = finalize_mpc(drivers, my_data)  # DBG
        # simply our share summed with total
        print("forwarding req: ", u)
        return finalize_mpc(drivers, my_data), []
