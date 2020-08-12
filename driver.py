class Driver:
    def __init__(self, full_name, license_id):
        self.fatigue = False
        self.full_name = full_name
        self.license_id = license_id
        self.last_hour = False
        self.last_quarters = [False, False, False, False]

    def set_fatigue(self, val):
        self.fatigue = val

    def set_last_hour(self, val):
        self.last_hour = val

    def set_last_quarters(self, values):
        self.last_quarters = [val for val in values[:4]]

    def get_fatigue(self):
        return self.fatigue

    def get_id(self):
        return str(self.full_name) + str(self.license_id)

    def get_last_hour(self):
        return self.last_hour

    def get_last_quarters(self):
        return self.last_quarters

    def __repr__(self):
        res = f"{self.full_name}\t{self.license_id}\t"
        res += f"{self.fatigue}\t{self.last_hour}\t{self.last_quarters}"
        return res
