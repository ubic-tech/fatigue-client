from random import randrange
from typing import List, Mapping

from repository.drivers_repository import DriverID, Share
from models.drivers import DriverShares
from config import AggregatorConfig

def get_rand_pair(secret: int) -> (int, int):
    """
    return a pair of random integers so that their sum == secret
    :param secret: integer to be split into 2 shares
    :return: a pair of base's components
    """
    assert secret < AggregatorConfig.MODULO, f"{secret} > {AggregatorConfig.MODULO}"
    share0 = randrange(AggregatorConfig.MODULO)
    share1 = (secret - share0) % AggregatorConfig.MODULO
    return share0, share1


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
        my_shares = my_data[driver.hash_id]  # no miss guarantee by caller
        ubic_shares = [driver.shares[j] + share for j, share in enumerate(my_shares)]
        ubic_drivers_shares.append(DriverShares(hash_id=driver.hash_id, shares=ubic_shares))
    return ubic_drivers_shares
