from models.drivers import DriverShares
from routers.drivers import all_zeroes


drivers_ok = [
    DriverShares(
        hash_id="b7c7470e59e2a2df1bfd0a4705488ee6fe0c5c125de15cccdfab0e00d6c03dc0",
        shares=[0]),
    DriverShares(
        hash_id="db3defda18fafc0c197740438051c690d98b551a7e449d66390d38fa2db09b77",
        shares=[1])
]

drivers_ok_many = [
    DriverShares(
        hash_id="b7c7470e59e2a2df1bfd0a4705488ee6fe0c5c125de15cccdfab0e00d6c03dc0",
        shares=[0, 1, 2, 3]),
    DriverShares(
        hash_id="db3defda18fafc0c197740438051c690d98b551a7e449d66390d38fa2db09b77",
        shares=[0, 1, 0, 1])
]

drivers_all_zeros = [
    DriverShares(
        hash_id="b7c7470e59e2a2df1bfd0a4705488ee6fe0c5c125de15cccdfab0e00d6c03dc0",
        shares=[0]),
    DriverShares(
        hash_id="db3defda18fafc0c197740438051c690d98b551a7e449d66390d38fa2db09b77",
        shares=[0])
]

drivers_zeros_many = [
    DriverShares(
        hash_id="b7c7470e59e2a2df1bfd0a4705488ee6fe0c5c125de15cccdfab0e00d6c03dc0",
        shares=[0, 0, 0, 0]),
    DriverShares(
        hash_id="db3defda18fafc0c197740438051c690d98b551a7e449d66390d38fa2db09b77",
        shares=[0, 0, 0, 0])
]

drivers_empty = []


def test_check_all_zeros():
    assert not all_zeroes(drivers_ok)
    assert not all_zeroes(drivers_ok_many)
    assert all_zeroes(drivers_all_zeros)
    assert all_zeroes(drivers_zeros_many)
    assert all_zeroes(drivers_empty)
