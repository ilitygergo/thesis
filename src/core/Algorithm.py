from abc import ABC, abstractmethod


class Algorithm(ABC):

    @abstractmethod
    def printName(self):
        pass
