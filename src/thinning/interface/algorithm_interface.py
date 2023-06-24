from abc import ABC, abstractmethod


class IAlgorithm(ABC):
    step = 0
    previousStep = None

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def after_processing(self):
        pass

    @abstractmethod
    def print_algorithm_name(self):
        pass
