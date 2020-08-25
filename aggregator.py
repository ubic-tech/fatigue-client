from idrivers_db import IDriversDB


class Aggregator:
    def __init__(self, hash_id: str, drivers_db: IDriversDB):
        self.hash_id = hash_id
        self.drivers_db = drivers_db  # provides interface for "/drivers/*" handlers
