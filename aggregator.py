from db.drivers_repository import DriversRepository


class Aggregator:
    def __init__(self, hash_id: str, drivers_db: DriversRepository):
        self.hash_id = hash_id
        self.drivers_db = drivers_db  # provides interface for "/drivers/*" handlers
