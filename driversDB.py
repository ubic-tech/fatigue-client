class Driver:
    """simple data structure to keep driver's data"""
    def __init__(self, full_name, license_id):
        # private data
        self.full_name = full_name
        self.license_id = license_id
        # business data
        self.fatigue = False
        self.last_hour = False
        self.last_quarters = [False, False, False, False]
        self.on_order = False

    def get_id(self):
        """emulates a hash function to get uuid for each driver
        by full name and license number"""
        return str(self.full_name) + str(self.license_id)

    def __repr__(self):
        res = f"{self.full_name}\t{self.license_id}\t"
        res += f"{self.fatigue}\t{self.last_hour}\t{self.last_quarters}"
        return res


class DriversDB:
    """emulates data base of drivers
    provides interface to set/get fields of Driver data
    adders emulate insert op
    setters emulate update op
    getters emulate select op
    todo: remove setters"""
    def __init__(self, *args, **kwargs):
        self.drivers_database = {}

    def add_driver(self, full_name, license_id):
        d = Driver(full_name, license_id)
        self.drivers_database[d.get_id()] = d

    def set_fatigue(self, driver_id, val):
        self.drivers_database[driver_id].set_fatigue(val)

    def set_last_hour(self, driver_id, val):
        self.drivers_database[driver_id].set_last_hour(val)

    def set_last_quarters(self, driver_id, values):
        self.drivers_database[driver_id].set_last_quarters(values)

    def set_order(self, driver_id, val):
        self.drivers_database[driver_id].set_on_order(val)

    def get_fatigue(self, driver_id):
        return self.drivers_database[driver_id].fatigue

    def get_online_hour(self, driver_id, timestamp) -> list:
        return self.drivers_database[driver_id].last_hour

    def get_online_quarters(self, driver_id, timestamp) -> list:
        return self.drivers_database[driver_id].last_quarters

    def get_on_order(self, driver_id, timestamp) -> list:
        return self.drivers_database[driver_id].on_order
