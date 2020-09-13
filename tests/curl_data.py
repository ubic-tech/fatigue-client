from uuid import UUID
from datetime import datetime

from models import drivers

headers = {
    "X-Request-Id": "xreq",
}

fatigue_request = drivers.FatigueBody(
    timestamp=datetime(year=2020, month=7, day=14, hour=16, minute=46),
    drivers=[
        drivers.DriverFatigue(hash_id="a",
                              online=50,
                              on_order=100),
        drivers.DriverFatigue(hash_id="b",
                              online=100,
                              on_order=50),
    ]
)

online_hourly_request = drivers.ControlBody(
    timestamp=datetime(year=2020, month=7, day=14, hour=16, minute=46),
    drivers=[
        drivers.DriverShares(
            hash_id="b7c7470e59e2a2df1bfd0a4705488ee6fe0c5c125de15cccdfab0e00d6c03dc0",
            shares=[0]),
        drivers.DriverShares(
            hash_id="db3defda18fafc0c197740438051c690d98b551a7e449d66390d38fa2db09b77",
            shares=[1])
    ],
    chain=[UUID("777aaaaa-1af0-489e-b761-d40344c12e70"),
           UUID("888aaaaa-1af0-489e-b761-d40344c12e70"),
           UUID("999aaaaa-1af0-489e-b761-d40344c12e70")]
)

history_hourly_request = drivers.ControlBody(
    timestamp=datetime(year=2020, month=7, day=14, hour=16, minute=46),
    drivers=[
        drivers.DriverShares(
            hash_id="c6f3ac57944a531490cd39902d0f777715fd005efac9a30622d5f5205e7f6894",
            shares=[0 for _ in range(24)]),
        drivers.DriverShares(
            hash_id="0dfcddb0440e967f05bb68ca09a5e2188b8abc36bfb5b95b83b88be59c42c6e7",
            shares=[0 for _ in range(24)]),
        drivers.DriverShares(
            hash_id="624b60c58c9d8bfb6ff1886c2fd605d2adeb6ea4da576068201b6c6958ce93f4",
            shares=[0 for _ in range(24)])
    ],
    chain=["777aaaaa-1af0-489e-b761-d40344c12e70",
           "888aaaaa-1af0-489e-b761-d40344c12e70",
           "999aaaaa-1af0-489e-b761-d40344c12e70"]
)

online_quarter_hourly_request = drivers.ControlBody(
    timestamp=datetime(year=2020, month=7, day=14, hour=16, minute=46),
    drivers=[
        drivers.DriverShares(
            hash_id="b17ef6d19c7a5b1ee83b907c595526dcb1eb06db8227d650d5dda0a9f4ce8cd9",
            shares=[0, 0, 0, 0]),
        drivers.DriverShares(
            hash_id="3d734d729009b74c011651eb24b06a74151fb99b8da5110295da8bb77ec3f92d",
            shares=[1, 1, 1, 1]),
        drivers.DriverShares(
            hash_id="6cb6d4b2fa122bf8bd63280061e4a230565fdec3ce03268caa2f48ccd931c691",
            shares=[0, 0, 1, 1])
    ],
    chain=["777aaaaa-1af0-489e-b761-d40344c12e70",
           "888aaaaa-1af0-489e-b761-d40344c12e70",
           "999aaaaa-1af0-489e-b761-d40344c12e70"]
)

on_order_request = drivers.ControlBody(
    timestamp=datetime(year=2020, month=7, day=14, hour=16, minute=46),
    start=datetime(year=2020, month=7, day=14, hour=17, minute=46),
    drivers=[
        drivers.DriverShares(
            hash_id="c6f3ac57944a531490cd39902d0f777715fd005efac9a30622d5f5205e7f6894",
            shares=[0]),
        drivers.DriverShares(
            hash_id="0dfcddb0440e967f05bb68ca09a5e2188b8abc36bfb5b95b83b88be59c42c6e7",
            shares=[26]),
        drivers.DriverShares(
            hash_id="624b60c58c9d8bfb6ff1886c2fd605d2adeb6ea4da576068201b6c6958ce93f4",
            shares=[7])
    ],
    chain=["777aaaaa-1af0-489e-b761-d40344c12e70",
           "888aaaaa-1af0-489e-b761-d40344c12e70",
           "999aaaaa-1af0-489e-b761-d40344c12e70"]
)
