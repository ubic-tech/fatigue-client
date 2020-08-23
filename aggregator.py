from driversDB import DriversDB


class Aggregator:
    def __init__(self, name, _id):
        self.name = name
        self.id = _id
        self.drivers_db = DriversDB()
        self.aggregators = {}  # {"hash_id": "url", ...}

    def add_driver(self, full_name, license_id):
        self.drivers_db.add_driver(full_name, license_id)

    def add_aggregator(self, hash_id, url):
        if hash_id != self.id:
            self.aggregators[hash_id] = url
