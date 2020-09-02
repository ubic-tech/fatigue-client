from core import get_next_endpoint_hash_id, OperationError
from config import AggregatorConfig as AggrConf


def test_positive():
    sets = [
        [AggrConf.AGGR_HASH_ID, "OK", "FAIL", "FAIL", "FAIL", ],
        ["FAIL", AggrConf.AGGR_HASH_ID, "OK", "FAIL", "FAIL", ],
        ["FAIL", "FAIL", AggrConf.AGGR_HASH_ID, "OK", "FAIL", ],
        ["FAIL", "FAIL", "FAIL", AggrConf.AGGR_HASH_ID, "OK", ],
    ]
    for s in sets:
        assert get_next_endpoint_hash_id(s) == "OK"


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
        ["FAIL", AggrConf.AGGR_HASH_ID, ],
        ["FAIL", "FAIL", "FAIL", "FAIL", "FAIL", AggrConf.AGGR_HASH_ID, ],
    ]
    for s in sets:
        assert get_next_endpoint_hash_id(s) == ""
