from driversDB import DriversDB


class Aggregator:
    def __init__(self, name, _id):
        self.name = name
        self.id = _id
        self.drivers_db = DriversDB()

    def add_driver(self, full_name, license_id):
        self.drivers_db.add_driver(full_name, license_id)
