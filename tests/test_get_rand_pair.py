from hypothesis import given
import hypothesis.strategies as st

from core.mpc import get_rand_pair, MODULO


@given(st.integers(min_value=0, max_value=MODULO - 1))
def test_get_rand_pair_positive(secret: int):
    share1, share2 = get_rand_pair(secret)
    print(share1, share2, secret, (share1 + share2) % MODULO)
    assert (share1 + share2) % MODULO == secret


@given(st.integers(min_value=MODULO))
def test_get_rand_pair_negative(secret: int):
    try:
        _, _ = get_rand_pair(secret)
    except AssertionError:
        assert True
        return
    assert False, f"if {secret} greater {MODULO} AssertionError is expected"
