from driver import Driver
drivers_base = [
    Driver("Rogue", 101),
    Driver("Tough", 202),
    Driver("Harsh", 303),
    Driver("Rough", 404),
    Driver("Rigid", 505),
]

DRIVERS = {v.get_id(): v for v in drivers_base}

if __name__ == "__main__":
    print(DRIVERS)
