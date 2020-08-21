from driversDB import DriversDB


class Aggregator:
    def __init__(self, name, _id):
        self.name = name
        self.id = _id
        self.drivers = DriversDB()

    def add_driver(self, full_name, license_id):
        self.drivers.add_driver(full_name, license_id)
