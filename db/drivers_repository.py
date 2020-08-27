from datetime import datetime
from abc import ABC, abstractmethod
from typing import Mapping, Iterable

DriverID = str
Share = int


class DriversRepository(ABC):
    @abstractmethod
    def get_hourly(self, ts: datetime,
                   drivers: Iterable[DriverID]) -> Mapping[DriverID, Share]:
        pass

    @abstractmethod
    def get_on_order(self, ts: datetime,
                     drivers: Iterable[DriverID]) -> Mapping[DriverID, Share]:
        pass

    @abstractmethod
    def get_quarter_hourly(self, ts: datetime,
                           drivers: Iterable[DriverID]) -> Mapping[DriverID, Iterable[Share]]:
        pass

    @abstractmethod
    def get_history_hourly(self, ts: datetime,
                           drivers: Iterable[DriverID]) -> Mapping[DriverID, Iterable[Share]]:
        pass
