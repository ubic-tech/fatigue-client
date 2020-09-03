from core import continue_mpc, finalize_mpc, mpc_strategy
from models.models import DriverData
from random import randint, seed
from datetime import datetime
from copy import deepcopy
from typing import List


def setup_module(_):
    seed(datetime.now().microsecond)


drivers_hash_ids = [x for x in "qwertyuiopasdfghjklzxcvbnm!@#$%^&*(()_+{}<>?/.,1234567890"]
self_db_data_sets = [
    {h: [randint(0, 1), ] for h in drivers_hash_ids},
    {h: [randint(-100, 100), ] for h in drivers_hash_ids},
    {h: [randint(0, 1) for _ in range(2)] for h in drivers_hash_ids},
    {h: [randint(-100, 100) for _ in range(2)] for h in drivers_hash_ids},
    {h: [randint(0, 1) for _ in range(4)] for h in drivers_hash_ids},
    {h: [randint(-100, 100) for _ in range(4)] for h in drivers_hash_ids},
    {h: [randint(0, 1) for _ in range(24)] for h in drivers_hash_ids},
    {h: [randint(-100, 100) for _ in range(24)] for h in drivers_hash_ids},
    {h: [randint(0, 1) for _ in range(101)] for h in drivers_hash_ids},
    {h: [randint(-1000, 1000) for _ in range(101)] for h in drivers_hash_ids},
    {h: [randint(0, 1) for _ in range(1010)] for h in drivers_hash_ids},
    # severe tests below
    # {h: [randint(-1000, 1000) for _ in range(1010)] for h in drivers_hash_ids},
    # {h: [randint(0, 1) for _ in range(10**5 + 1)] for h in drivers_hash_ids},
    # {h: [randint(-(10**24), 10**24) for _ in range(10**5 - 1)] for h in drivers_hash_ids},
]


def get_request_data(hash_ids: List[str], shares_count: int)\
        -> List[DriverData]:
    return [
        DriverData(hash_id=h, shares=[
            randint(-1000, 1000) for _ in range(shares_count)
        ]) for h in hash_ids
    ]


def continue_mpc_validator(request_data, self_db_data, shares_len, processed_request_data, for_ubic):
    assert len(for_ubic) == len(processed_request_data)

    for r, p, u in zip(request_data, processed_request_data, for_ubic):
        assert p.hash_id == u.hash_id == r.hash_id
        assert len(p.shares) == len(u.shares) == len(r.shares) == shares_len
        hash_id = p.hash_id
        db_shares = self_db_data[hash_id]
        assert shares_len == len(db_shares)
        for i in range(shares_len):
            web_part = u.shares[i] + p.shares[i]
            db_part = r.shares[i] + db_shares[i]
            assert web_part == db_part


def continue_mpc_helper(request_data, self_db_data, shares_len):
    processed_request_data = deepcopy(request_data)
    for_ubic = continue_mpc(processed_request_data, self_db_data)
    continue_mpc_validator(request_data,
                           self_db_data,
                           shares_len,
                           processed_request_data,
                           for_ubic)


def finalize_mpc_validator(request_data, self_db_data, shares_len, processed_request_data):
    for r, p in zip(request_data, processed_request_data):
        assert r.hash_id == p.hash_id
        hash_id = r.hash_id
        db_shares = self_db_data[hash_id]
        assert len(db_shares) == len(r.shares) == len(p.shares) == shares_len
        for i in range(shares_len):
            assert db_shares[i] + r.shares[i] == p.shares[i]


def finalize_mpc_helper(request_data, self_db_data, shares_len):
    processed_request_data = deepcopy(request_data)
    finalize_mpc(processed_request_data, self_db_data)
    finalize_mpc_validator(request_data, self_db_data, shares_len, processed_request_data)


def test_mpc():
    endpoint_hash_ids = ["", "a", ]
    for self_db_data in self_db_data_sets:
        shares_len = len(self_db_data[drivers_hash_ids[0]])  # lens should be equal
        request_data = get_request_data(drivers_hash_ids, shares_len)

        continue_mpc_helper(request_data, self_db_data, shares_len)
        finalize_mpc_helper(request_data, self_db_data, shares_len)
        for endpoint_hash_id in endpoint_hash_ids:
            original_request_data = deepcopy(request_data)
            for_ubic, request_data = mpc_strategy(request_data, self_db_data, endpoint_hash_id)
            if endpoint_hash_id:
                continue_mpc_validator(original_request_data, self_db_data, shares_len, request_data, for_ubic)
            else:
                finalize_mpc_validator(original_request_data, self_db_data, shares_len, request_data)
