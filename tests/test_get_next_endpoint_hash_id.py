from mpc.mpc import get_next_endpoint_hash_id, OperationError
from config import AggregatorConfig as AggrConf
from copy import deepcopy


def test_positive():
    sets = [
        [AggrConf.AGGR_HASH_ID, "OK", "FAIL", "FAIL", "FAIL", ],
        [AggrConf.AGGR_HASH_ID, "OK", "FAIL", ],
        [AggrConf.AGGR_HASH_ID, "OK", ],
    ]
    for i, s in enumerate(deepcopy(sets)):
        assert get_next_endpoint_hash_id(s) == "OK"
        assert s == sets[i][1:]  # testing popping


def test_self_not_found():
    sets = [
        [],
        ["FAIL", ],
        ["FAIL", "FAIL", "FAIL", "FAIL", "FAIL", ],
    ]
    for s in sets:
        try:
            get_next_endpoint_hash_id(s)
            assert False
        except OperationError:
            assert True


def test_self_last():
    sets = [
        [AggrConf.AGGR_HASH_ID, ],
    ]
    for s in sets:
        assert get_next_endpoint_hash_id(s) == ""
        assert s == []
