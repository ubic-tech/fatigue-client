class Driver:
    """simple data structure to keep driver's data"""
    def __init__(self, full_name, license_id):
        self.fatigue = False
        self.full_name = full_name
        self.license_id = license_id
        self.last_hour = False
        self.last_quarters = [False, False, False, False]

    def get_id(self):
        """emulates a hash function to get uuid for each driver
        by full name and license number"""
        return str(self.full_name) + str(self.license_id)

    def __repr__(self):
        res = f"{self.full_name}\t{self.license_id}\t"
        res += f"{self.fatigue}\t{self.last_hour}\t{self.last_quarters}"
        return res


class DriversDB:
    """
    emulates data base of drivers
    provides interface to set/get fields of Driver data structure
    """
    def __init__(self):
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

    def get_fatigue(self, driver_id):
        return self.drivers_database[driver_id].fatigue

    def get_last_hour(self, driver_id):
        return self.drivers_database[driver_id].last_hour

    def get_last_quarters(self, driver_id):
        return self.drivers_database[driver_id].last_quarters
