import abc
from abc import ABC


class Algorithm(ABC):
    @abc.abstractmethod
    def step(self):
        pass

    @abc.abstractmethod
    def clear_helpers(self):
        pass

    @abc.abstractmethod
    def print_algorithm_name(self):
        pass
