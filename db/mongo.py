from db.drivers_repository import *


class Mongo(DriversRepository):
    def get_hourly(self, ts: datetime, ids: Sequence[str]) -> Dict[str, int]:
        pass

    def get_on_order(self, ts: datetime, ids: Sequence[str]) -> Dict[str, int]:
        pass

    def get_quarter_hourly(self, ts: datetime,
                           ids: Sequence[str]) -> Dict[str, Tuple[int, int, int, int]]:
        pass

    def get_history_hourly(self, ts: datetime, ids: Sequence[str]) -> Dict[str, Sequence[int]]:
        pass
