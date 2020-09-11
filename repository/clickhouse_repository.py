from datetime import datetime
from typing import Mapping, Iterable

from clickhouse_driver import Client

from repository.drivers_repository import DriverID, Share, DriversRepository


def init_static(cls):
    cls._init_static()
    return cls


@init_static
class ClickhouseRepository(DriversRepository):

    _history_conditions: str = ''

    @classmethod
    def _init_static(cls):
        conditions = []
        for h in reversed(range(1, 25)):
            conditions.append(
                'countIf(timestamp between toStartOfFifteenMinutes(toDateTime(%(start)s)) - ' +
                f"INTERVAL {59 * h} MINUTE " +
                'and toStartOfFifteenMinutes(toDateTime(%(start)s)) - ' +
                f"INTERVAL {59 * (h - 1)} MINUTE)"
            )
        cls._history_conditions = ',\n'.join(conditions)

    def __init__(self, host: str, operator: str = 'Yandex'):
        self._operator = operator
        self._client = Client(host=host)

    @staticmethod
    def make_dict(cursor, norm=True):
        d = {}
        for row in cursor:
            d[row[0]] = list(map(lambda x: int(bool(x)), row[1:])) if norm else list(row[1:])
        return d

    def get_drivers(self) -> Iterable[DriverID]:

        return self._client.execute(
            query='SELECT DISTINCT driver from drivers',
            columnar=True
        )[0]

    def get_hourly(self,
                   drivers: Iterable[DriverID],
                   start: datetime) -> Mapping[DriverID, Iterable[Share]]:

        return self.make_dict(self._client.execute_iter(
            query=(
                'SELECT'
                '  driver,'
                '  countIf(timestamp between '
                '    toStartOfFifteenMinutes(toDateTime(%(start)s)) - INTERVAL 59 MINUTE' 
                '    and toStartOfFifteenMinutes(toDateTime(%(start)s))) as h '
                'FROM drivers'
                '  WHERE driver in %(drivers)s and state = %(state)s '
                'GROUP BY driver'
            ),
            params={
                'start': start,
                'drivers': drivers,
                'state': self._operator,
            }
        ))

    def get_on_order(self,
                     drivers: Iterable[DriverID],
                     start: datetime, end: datetime) -> Mapping[DriverID, Iterable[Share]]:

        return self.make_dict(self._client.execute_iter(
            query=(
                'SELECT'
                '  driver,'
                '  countIf(timestamp between '
                '    toStartOfFifteenMinutes(toDateTime(%(start)s)) and '
                '    toStartOfFifteenMinutes(toDateTime(%(end)s))) as duration '
                'FROM drivers'
                '  WHERE driver in %(drivers)s and state = %(state)s '
                'GROUP BY driver'
            ),
            params={
                'start': start,
                'end': end,
                'drivers': drivers,
                'state': self._operator,
            }
        ), norm=False)

    def get_quarter_hourly(self,
                           drivers: Iterable[DriverID],
                           start: datetime) -> Mapping[DriverID, Iterable[Share]]:

        return self.make_dict(self._client.execute_iter(
            query=(
                'SELECT'
                '  driver,'
                '  countIf(toStartOfFifteenMinutes(timestamp) = '
                '    toStartOfFifteenMinutes(toDateTime(%(start)s)) - INTERVAL 1 HOUR) as i1,'
                '  countIf(toStartOfFifteenMinutes(timestamp) = '
                '    toStartOfFifteenMinutes(toDateTime(%(start)s)) - INTERVAL 45 MINUTE) as i2,'
                '  countIf(toStartOfFifteenMinutes(timestamp) = '
                '    toStartOfFifteenMinutes(toDateTime(%(start)s)) - INTERVAL 30 MINUTE) as i3,'
                '  countIf(toStartOfFifteenMinutes(timestamp) = '
                '    toStartOfFifteenMinutes(toDateTime(%(start)s)) - INTERVAL 30 MINUTE) as i4 '
                'FROM drivers'
                '  WHERE driver in %(drivers)s and state = %(state)s '
                'GROUP BY driver'
            ),
            params={
                'start': start,
                'drivers': drivers,
                'state': self._operator,
            }
        ))

    def get_history_hourly(self,
                           drivers: Iterable[DriverID],
                           start: datetime) -> Mapping[DriverID, Iterable[Share]]:

        return self.make_dict(self._client.execute_iter(
            query=(
                'SELECT'
                '  driver,'
                f" {self._history_conditions} "
                'FROM drivers '
                '  WHERE driver in %(drivers)s and state = %(state)s '
                'GROUP BY driver'
            ),
            params={
                'start': start,
                'drivers': drivers,
                'state': self._operator,
            }
        ))
