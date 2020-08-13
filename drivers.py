from driver import Driver
from config import DRIVERS_DATA
drivers_base = [
    Driver(name, license_id) for name, license_id in DRIVERS_DATA
]

DRIVERS = {v.get_id(): v for v in drivers_base}

if __name__ == "__main__":
    print(DRIVERS)
