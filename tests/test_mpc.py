from hypothesis import given, strategies as st
from typing import Tuple, List, Dict, Iterable, Mapping

from core.mpc import continue_mpc, finalize_mpc
from models.drivers import DriverShares
from repository.drivers_repository import DriverID, Share
from config import AggregatorConfig


HOURLY = 1
QUARTER_HOURLY = 4
HISTORY_HOURLY = 24
MAX_RANDOM_VALUE = AggregatorConfig.MODULO - 1


def continue_mpc_validator(request_data: List[DriverShares],
                           my_data: Mapping[DriverID, Iterable[Share]]):
    for_ubic, for_next_aggr = continue_mpc(request_data, my_data)

    assert (
        len(for_ubic) ==
        len(for_next_aggr) ==
        len(request_data) ==
        len(my_data)
    )

    for x in range(len(for_ubic)):
        driver_id = for_ubic[x].hash_id
        ubic_shares = for_ubic[x].shares
        next_aggr_shares = for_next_aggr[x].shares
        request_shares = request_data[x].shares
        real_data = list(my_data[driver_id])
        assert(
            len(ubic_shares) ==
            len(next_aggr_shares) ==
            len(request_shares) ==
            len(real_data)
        )

        for y in range(len(real_data)):
            target = ((ubic_shares[y] + next_aggr_shares[y]) -
                      request_shares[y]) % AggregatorConfig.MODULO
            assert real_data[y] == target


def finalize_mpc_validator(request_data: List[DriverShares],
                           my_data: Mapping[DriverID, Iterable[Share]]):
    for_ubic = finalize_mpc(request_data, my_data)

    assert (
        len(for_ubic) ==
        len(request_data) ==
        len(my_data)
    )

    for x in range(len(for_ubic)):
        driver_id = for_ubic[x].hash_id
        ubic_shares = for_ubic[x].shares
        request_shares = request_data[x].shares
        real_data = list(my_data[driver_id])
        assert (
                len(ubic_shares) ==
                len(request_shares) ==
                len(real_data)
        )

        for y in range(len(real_data)):
            target = (ubic_shares[y] - request_shares[y]) % \
                     AggregatorConfig.MODULO
            assert real_data[y] == target


def compute(data: Dict[str, Tuple[List[int], List[int]]]):
    my_data = {str(k): v[0] for k, v in data.items()}

    request_data = [
        DriverShares(hash_id=str(k), shares=v[1]) for k, v in data.items()
    ]

    continue_mpc_validator(request_data, my_data)
    finalize_mpc_validator(request_data, my_data)


@given(st.dictionaries(
    st.uuids(),
    st.tuples(
        st.lists(
            st.integers(min_value=0, max_value=MAX_RANDOM_VALUE),
            min_size=HOURLY, max_size=HOURLY
        ),
        st.lists(
            st.integers(min_value=0, max_value=MAX_RANDOM_VALUE),
            min_size=HOURLY, max_size=HOURLY
        ),
    ),
    min_size=1
))
def test_1_share(data: Dict[str, Tuple[List[int], List[int]]]):
    compute(data)


@given(st.dictionaries(
    st.uuids(),
    st.tuples(
        st.lists(
            st.integers(min_value=0, max_value=MAX_RANDOM_VALUE),
            min_size=QUARTER_HOURLY, max_size=QUARTER_HOURLY
        ),
        st.lists(
            st.integers(min_value=0, max_value=MAX_RANDOM_VALUE),
            min_size=QUARTER_HOURLY, max_size=QUARTER_HOURLY
        ),
    ),
    min_size=1
))
def test_4_share(data: Dict[str, Tuple[List[int], List[int]]]):
    compute(data)


@given(st.dictionaries(
    st.uuids(),
    st.tuples(
        st.lists(
            st.integers(min_value=0, max_value=MAX_RANDOM_VALUE),
            min_size=HISTORY_HOURLY, max_size=HISTORY_HOURLY
        ),
        st.lists(
            st.integers(min_value=0, max_value=MAX_RANDOM_VALUE),
            min_size=HISTORY_HOURLY, max_size=HISTORY_HOURLY
        ),
    ),
    min_size=1
))
def test_24_share(data: Dict[str, Tuple[List[int], List[int]]]):
    compute(data)
