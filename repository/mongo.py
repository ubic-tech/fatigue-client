from db.drivers_repository import *


class Mongo(DriversRepository):
    def __init__(self):
        super().__init__()

    def get_hourly(self, ts: datetime,
                   drivers: Iterable[DriverID]) -> Mapping[DriverID, Share]:
        pass

    def get_on_order(self, ts: datetime,
                     drivers: Iterable[DriverID]) -> Mapping[DriverID, Share]:
        pass

    def get_quarter_hourly(self, ts: datetime,
                           drivers: Iterable[DriverID]) -> Mapping[DriverID, Iterable[Share]]:
        pass

    def get_history_hourly(self, ts: datetime,
                           drivers: Iterable[DriverID]) -> Mapping[DriverID, Iterable[Share]]:
        pass
