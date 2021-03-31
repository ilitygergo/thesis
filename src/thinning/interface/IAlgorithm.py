from abc import ABC, abstractmethod


class IAlgorithm(ABC):
    step = 0
    previousStep = None

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def processStepOnImage(self, img):
        pass
