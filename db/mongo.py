from db.idrivers import IDriversDB


class Mongo(IDriversDB):
    def __init__(self, *argc, **kwargs):
        pass

    def handle_fatigue(self, *args, **kwargs):
        pass

    def get_online_hour(self, driver_id, timestamp) -> list:
        return []

    def get_online_quarters(self, driver_id, timestamp) -> list:
        return []

    def get_on_order(self, driver_id, timestamp) -> list:
        return []
