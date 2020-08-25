from abc import ABC, abstractmethod


class IDriversDB(ABC):
    """emulates data base of drivers
    provides interface to set/get fields of Driver data
    getters emulate select op"""

    @abstractmethod
    def handle_fatigue(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_online_hour(self, driver_id, timestamp) -> list:
        pass

    @abstractmethod
    def get_online_quarters(self, driver_id, timestamp) -> list:
        pass

    @abstractmethod
    def get_on_order(self, driver_id, timestamp) -> list:
        pass
