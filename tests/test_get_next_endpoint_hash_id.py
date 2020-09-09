from copy import deepcopy

from utils.utils import OperationError
from routers.drivers import get_next_endpoint_uuid


MY_HASH_ID = "MY_HASH"


def test_positive():
    sets = [
        [MY_HASH_ID, "OK", "FAIL", "FAIL", "FAIL", ],
        [MY_HASH_ID, "OK", "FAIL", ],
        [MY_HASH_ID, "OK", ],
    ]
    for i, s in enumerate(deepcopy(sets)):
        assert get_next_endpoint_uuid(s, MY_HASH_ID) == "OK"
        assert s == sets[i][1:]  # testing popping


def test_self_not_found():
    sets = [
        [],
        ["FAIL", ],
        ["FAIL", "FAIL", "FAIL", "FAIL", "FAIL", ],
    ]
    for s in sets:
        try:
            get_next_endpoint_uuid(s, MY_HASH_ID)
            assert False
        except OperationError:
            assert True


def test_self_last():
    sets = [
        [MY_HASH_ID, ],
    ]
    for s in sets:
        assert get_next_endpoint_uuid(s, MY_HASH_ID) == ""
        assert s == []
