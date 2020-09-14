from abc import ABCMeta, abstractmethod

import numpy as np


class State(metaclass=ABCMeta):
    def __init__(self, index, profile):
        self._index = index
        self._profile = profile

    @property
    def index(self):
        return self._index

    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def next_state(self):
        return self._profile.next_state(self)

    def __str__(self):
        return self.name


class PendingState(State):
    def __init__(self, index, profile, generator):
        super().__init__(index, profile)
        self._timeout = generator()

    @property
    def timeout(self):
        return self._timeout

    def next_state(self):
        assert self._timeout > 0
        self._timeout -= 1
        if self._timeout > 0:
            return self
        
        return super().next_state()
    
    def __str__(self):
        return f'{self.name}: {self.timeout}'


class Rest(PendingState):

    # We're modeling that by exponential distrubution with lambda = .007
    # 16M rides a month, 50K cars -> 16M/50k/30/24/60 ~ .007
    generator = lambda _: np.rint(np.positive(np.random.exponential(1/.007))) + 1.

    def __init__(self, index, profile):
        super().__init__(index, profile, self.generator)

class OrderState(PendingState):
    
    rides = np.load('data/rides.npy')
    
    @classmethod
    def generator(cls):
        return np.random.choice(
            np.rint(cls.rides[0]),
            p=cls.rides[1],
        )

    def __init__(self, index, profile):
        super().__init__(index, profile, self.generator)

class Yandex(OrderState):
    def __init__(self, index, profile):
        super().__init__(index, profile)

class City(OrderState):
    def __init__(self, index, profile):
        super().__init__(index, profile)

class Gett(OrderState):
    def __init__(self, index, profile):
        super().__init__(index, profile)

class Profile:
    __states = [
        Rest,
        Yandex,
        City,
        Gett,
    ]

    def __init__(self, transitions: np.ndarray):
        assert (
            transitions.shape[0] ==
            transitions.shape[1] ==
            len(Profile.__states)
        )
        self._transitions = transitions
        self._sd = self.stable_distr()

    def next_state(self, state: State = None) -> State:
        if state is not None:
            distr = self._transitions[state.index]
        else:
            distr = self._sd

        index = np.random.choice(
            len(Profile.__states),
            p=distr
        )

        return Profile.__states[index](index, self)

    def stable_distr(self):
        distr = np.zeros(self._transitions.shape[0])
        distr[0] = 1.
        for _ in range(64):
            distr = np.dot(distr, self._transitions)
        return distr
