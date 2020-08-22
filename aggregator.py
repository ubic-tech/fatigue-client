from driversDB import DriversDB


class Aggregator:
    def __init__(self, name, _id):
        self.name = name
        self.id = _id
        self.drivers = DriversDB()
        self.aggregators = {}  # {"hash_id": "url", ...}

    def add_driver(self, full_name, license_id):
        self.drivers.add_driver(full_name, license_id)

    def add_aggregator(self, hash_id, url):
        if hash_id != self.id:
            self.aggregators[hash_id] = url
