from abc import ABC, abstractmethod
from src.thinning.interface.IAlgorithm import IAlgorithm
from src.thinning.DyerRosenfeld import DyerRosenfeld
from src.thinning.SalariSiy import SalariSiy
from src.thinning.Kang import Kang
from src.thinning.Kim import Kim
from src.thinning.Couprie import Couprie
from src.thinning.Image import Image


class AlgorithmFactory(ABC):
    @abstractmethod
    def factory(self):
        pass

    def runAlgorithm(self):
        img = Image.getInstance()
        algorithm = self.factory()

        while not algorithm.processStepOnImage(img).isEqualTo(algorithm.previousStep):
            pass


class DyerRosenfeldFactory(AlgorithmFactory):
    def factory(self) -> IAlgorithm:
        return DyerRosenfeld()


class SalariSiyFactory(AlgorithmFactory):
    def factory(self) -> IAlgorithm:
        return SalariSiy()


class KangFactory(AlgorithmFactory):
    def factory(self) -> IAlgorithm:
        return Kang()


class KimFactory(AlgorithmFactory):
    def factory(self) -> IAlgorithm:
        return Kim()


class CouprieFactory(AlgorithmFactory):
    def factory(self) -> IAlgorithm:
        return Couprie()
