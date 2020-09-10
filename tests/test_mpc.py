from random import randint, seed
from datetime import datetime

from hypothesis import given, strategies as st
from typing import List, Dict, Iterable

from core.mpc import continue_mpc, finalize_mpc
from models.drivers import DriverShares


def setup_module(_):
    seed(datetime.now().microsecond)


def get_request_data(
        hash_ids: Iterable[str],
        shares_count: int
) -> List[DriverShares]:
    return [
        DriverShares(hash_id=h, shares=[
            randint(-1000, 1000) for _ in range(shares_count)
        ]) for h in hash_ids
    ]


def continue_mpc_validator(request_data, my_data, shares_count):
    for_ubic, for_next_aggr = continue_mpc(request_data, my_data)
    assert len(for_ubic) == len(for_next_aggr)

    for r, a, u in zip(request_data, for_next_aggr, for_ubic):
        assert a.hash_id == u.hash_id == r.hash_id
        assert len(a.shares) == len(u.shares) == len(r.shares) == shares_count
        hash_id = a.hash_id
        db_shares = my_data[hash_id]
        assert shares_count == len(db_shares)
        for i in range(shares_count):
            web_part = u.shares[i] + a.shares[i]
            db_part = r.shares[i] + db_shares[i]
            assert web_part == db_part


def finalize_mpc_validator(request_data, my_data, shares_count):
    for_next_aggr = finalize_mpc(request_data, my_data)
    for r, a in zip(request_data, for_next_aggr):
        assert r.hash_id == a.hash_id
        hash_id = r.hash_id
        db_shares = my_data[hash_id]
        assert len(db_shares) == len(r.shares) == len(a.shares) == shares_count
        for i in range(shares_count):
            assert db_shares[i] + r.shares[i] == a.shares[i]


def compute(data: Dict[str, List[int]], shares_count: int):
    data = {str(k): v for k, v in data.items()}
    request_data = get_request_data(data.keys(), shares_count)
    continue_mpc_validator(request_data, data, shares_count)
    finalize_mpc_validator(request_data, data, shares_count)


@given(st.dictionaries(st.uuids(), st.lists(st.integers(), min_size=0, max_size=0)))
def test_0_share(data: Dict[str, List[int]]):
    compute(data, 0)


@given(st.dictionaries(st.uuids(), st.lists(st.integers(), min_size=1, max_size=1)))
def test_1_share(data: Dict[str, List[int]]):
    compute(data, 1)


@given(st.dictionaries(st.uuids(), st.lists(st.integers(), min_size=4, max_size=4)))
def test_4_shares(data: Dict[str, List[int]]):
    compute(data, 4)


@given(st.dictionaries(st.uuids(), st.lists(st.integers(), min_size=24, max_size=24)))
def test_24_shares(data: Dict[str, List[int]]):
    compute(data, 24)
