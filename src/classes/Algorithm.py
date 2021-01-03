from abc import ABC, abstractmethod


class Algorithm(ABC):
    @abstractmethod
    def getName(self) -> str:
        pass
