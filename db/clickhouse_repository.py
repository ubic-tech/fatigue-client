from datetime import datetime
from typing import Mapping, Iterable
from clickhouse_driver import Client
from db.drivers_repository import DriverID, Share, DriversRepository


def init_static(cls):
    cls.init_static()
    return cls


@init_static
class ClickhouseRepository(DriversRepository):
    _history_conditions: str = ''

    @classmethod
    def init_static(cls):
        conds = []
        for h in reversed(range(1, 25)):
            conds.append(
                "countIf(timestamp between toStartOfFifteenMinutes(toDateTime('{0}')) - " +
                f"INTERVAL {59*h} MINUTE " +
                "and toStartOfFifteenMinutes(toDateTime('{0}')) - " +
                f"INTERVAL {59*(h - 1)} MINUTE)"
            )
        cls._history_conditions = ',\n'.join(conds)

    def __init__(self, host: str, operator: str = 'Yandex'):
        self._operator = operator
        self._client = Client(host=host)

    @staticmethod
    def make_dict(cursor, norm=True):
        d = {}
        for row in cursor:
            d[row[0]] = list(map(lambda x: int(bool(x)), row[1:])) if norm else row[1:]
        return d
    
    def get_drivers(self) -> Iterable[DriverID]:
        _q = 'select distinct driver from default.drivers'
        return self._client.execute(_q, columnar=True)[0]

    def _get_hourly(self, ts: datetime,
                    drivers: Iterable[DriverID]) -> Mapping[DriverID, Iterable[Share]]:
        _r15 = 'toStartOfFifteenMinutes'
        _q = (
            'SELECT'
            '  driver,'
           f"  countIf(timestamp between {_r15}(toDateTime('{ts}')) - INTERVAL 59 MINUTE and {_r15}(toDateTime('{ts}'))) as h "
            'FROM drivers'
           f"  WHERE driver in {drivers} and state = '{self._operator}' "
            'GROUP BY driver' 
        )
        return self._client.execute_iter(_q)

    def get_hourly(self, ts: datetime,
                   drivers: Iterable[DriverID]) -> Mapping[DriverID, Iterable[Share]]:
        return self.make_dict(self._get_hourly(ts, drivers))
    
    def get_on_order(self, ts: datetime,
                     drivers: Iterable[DriverID],
                     start: datetime) -> Mapping[DriverID, Iterable[Share]]:
        return self.make_dict(self._get_hourly(ts, drivers), norm=False)
    
    def get_quarter_hourly(self, ts: datetime,
                           drivers: Iterable[DriverID]) -> Mapping[DriverID, Iterable[Share]]:
        
        _r15 = 'toStartOfFifteenMinutes'
        _q = (
           'SELECT'
           '  driver,'
           f"  countIf({_r15}(timestamp) = {_r15}(toDateTime('{ts}')) - INTERVAL 1 HOUR) as i1,"
           f"  countIf({_r15}(timestamp) = {_r15}(toDateTime('{ts}')) - INTERVAL 45 MINUTE) as i2,"
           f"  countIf({_r15}(timestamp) = {_r15}(toDateTime('{ts}')) - INTERVAL 30 MINUTE) as i3,"
           f"  countIf({_r15}(timestamp) = {_r15}(toDateTime('{ts}')) - INTERVAL 30 MINUTE) as i4 "
           'FROM drivers'
           f"  WHERE driver in {drivers} and state = '{self._operator}' "
           'GROUP BY driver'
        )

        return self.make_dict(self._client.execute_iter(_q))
    
    def get_history_hourly(self, ts: datetime,
                           drivers: Iterable[DriverID]) -> Mapping[DriverID, Iterable[Share]]:

        _q = (
            'SELECT'
            '  driver,'
            f' {self._history_conditions.format(ts)} '
            'FROM drivers '
            f" WHERE driver in {drivers} and state = '{self._operator}' "
            'GROUP BY driver'
        )
    
        return self.make_dict(self._client.execute_iter(_q))
