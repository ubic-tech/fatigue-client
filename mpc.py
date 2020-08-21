from random import randint, seed
from datetime import datetime
LAST_INDEX = -1


class Ubic(object):
    def __init__(self):
        super(Ubic, self).__init__()
        self._sum = 0

    def add(self, _part):
        self._sum += _part

    def get_sum(self):
        return self._sum


class Mpc:
    def __init__(self, value, _ubic):
        self._value = value
        self._ubic = _ubic

    def value(self):
        return self._value

    def _get_rand_pair(self):
        seed(datetime.now().microsecond)
        f = randint(1000, 2000)
        s = self.value() - f
        return (f, s) if randint(0, 1) else (s, f)

    def process(self, index, _part):
        if index == LAST_INDEX:
            return _part + self.value()

        f, s = self._get_rand_pair()
        self._ubic[0].add(f)
        return part + s


if __name__ == '__main__':
    ubic = [Ubic(), ]
    aggr = [Mpc(10, ubic), Mpc(0, ubic), Mpc(21, ubic), ]
    aggr_len = len(aggr)
    part = 0

    for i, agr in enumerate(aggr):
        if i == aggr_len - 1:
            part = agr.process(LAST_INDEX, part)
        else:
            part = agr.process(i, part)
    res = abs(part) - abs(ubic[0].get_sum())
    print(part, ", ", ubic[0].get_sum(), "\tres = ", abs(res))
