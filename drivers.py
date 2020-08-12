class Driver:
    def __init__(self, name, license_id):
        self.fatigue = False
        self.name = name
        self.license_id = license_id
        self.last_hour = True
        self.last_quarters = [True, True, True, True]

    def set_fatigue(self, val):
        self.fatigue = val
