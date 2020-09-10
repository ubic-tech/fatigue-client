from copy import deepcopy
from uuid import UUID

from utils.utils import OperationError
from routers.drivers import get_next_endpoint_uuid


MY_UUID_STR = "8704d129-1af0-489e-b761-d40344c12e70"
MY_UUID = UUID(MY_UUID_STR)
NEXT_UUID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")


def test_positive():
    sets = [
        [
            MY_UUID, NEXT_UUID,
            UUID("87a4d1b9-1afc-4d9e-b161-d20445c16e70"),
            UUID("0075c51d-3df1-4d2b-8d98-66cbd25af2a0"),
            UUID("431cb246-683d-4ed7-a9fd-4384c72d3604"),
        ],
        [
            MY_UUID, NEXT_UUID,
            UUID("0075c51d-3df1-4d2b-8d98-66cbd25af2a0"),
            UUID("431cb246-683d-4ed7-a9fd-4384c72d3604"),
        ],
        [
            MY_UUID, NEXT_UUID,
        ],
    ]
    for i, s in enumerate(deepcopy(sets)):
        assert get_next_endpoint_uuid(s, MY_UUID_STR) == str(NEXT_UUID)
        assert s == sets[i][1:]  # test popping


def test_not_found():
    sets = [
        [],
        [UUID("87a4d1b9-1afc-4d9e-b161-d20445c16e70"), ],
        [
            UUID("87a4d1b9-1afc-4d9e-b161-d20445c16e70"),
            UUID("0075c51d-3df1-4d2b-8d98-66cbd25af2a0"),
            UUID("431cb246-683d-4ed7-a9fd-4384c72d3604"),
        ],
    ]
    for s in sets:
        try:
            get_next_endpoint_uuid(s, MY_UUID_STR)
            assert False
        except OperationError:
            assert True


def test_last():
    chain = [MY_UUID, ]
    assert get_next_endpoint_uuid(chain, MY_UUID_STR) is None
    assert chain == []
