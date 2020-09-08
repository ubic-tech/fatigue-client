from hypothesis import given
import hypothesis.strategies as st
from mpc.mpc import get_rand_pair


@given(st.integers())
def test_get_rand_pair(number: int):
    f, s = get_rand_pair(number)
    assert f + s == number
