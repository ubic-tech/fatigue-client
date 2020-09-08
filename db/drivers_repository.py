from datetime import datetime
from abc import ABC, abstractmethod
from typing import Mapping, Iterable

DriverID = str
Share = int


class DriversRepository(ABC):
    @abstractmethod
    def get_hourly(self,
                   drivers: Iterable[DriverID],
                   start: datetime) -> Mapping[DriverID, Iterable[Share]]:
        pass

    @abstractmethod
    def get_on_order(self,
                     drivers: Iterable[DriverID],
                     start: datetime, end: datetime) -> Mapping[DriverID, Iterable[Share]]:
        pass

    @abstractmethod
    def get_quarter_hourly(self,
                           drivers: Iterable[DriverID],
                           start: datetime) -> Mapping[DriverID, Iterable[Share]]:
        pass

    @abstractmethod
    def get_history_hourly(self,
                           drivers: Iterable[DriverID],
                           start: datetime) -> Mapping[DriverID, Iterable[Share]]:
        pass
