from datetime import datetime, timedelta
import hashlib
import csv
import sys

import click
import numpy as np

from repo_filler.states import Rest, Profile, OrderState


def create_profile() -> Profile:
    return Profile(
        np.array([
            [.1, .4, .3, .2],
            [.3, .7, .0, .0],
            [.4, .0, .6, .0],
            [.5, .0, .0, .5],
        ])
    )


def generate_id(x: str) -> str:
    return hashlib.sha256(x.encode('utf-8')).hexdigest()


@click.command()
@click.option('--start', type=click.DateTime(), default='2020-07-01T00:00:00')
@click.option('--end', type=click.DateTime(), default='2020-07-31T00:00:00')
@click.option('--drivers', type=int, default=1000)
def main(start: datetime, end: datetime, drivers: int):
    assert (start < end)
    assert (drivers > 0)

    writer = csv.writer(sys.stdout)
    # writer.writerow(['driver_id', 'timestamp', 'state'])

    for x in range(drivers):

        driver_id = generate_id(str(x))
        profile = create_profile()

        state = profile.next_state()
        currt = start
        while currt < end:
            writer.writerow([currt, driver_id, state.name])
            currt += timedelta(minutes=1)
            state = state.next_state()


if __name__ == "__main__":
    main()
