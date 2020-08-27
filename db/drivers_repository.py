from datetime import datetime
from abc import ABCMeta, abstractmethod
from typing import Dict, Sequence, Tuple


class DriversRepository(ABCMeta):
    """interface class"""

    @abstractmethod
    def get_hourly(self, ts: datetime, ids: Sequence[str]) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_on_order(self, ts: datetime, ids: Sequence[str]) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_quarter_hourly(self, ts: datetime,
                           ids: Sequence[str]) -> Dict[str, Tuple[int, int, int, int]]:
        pass

    @abstractmethod
    def get_history_hourly(self, ts: datetime, ids: Sequence[str]) -> Dict[str, Sequence[int]]:
        pass
