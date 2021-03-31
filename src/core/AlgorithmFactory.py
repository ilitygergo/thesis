import bcolors
from abc import ABC, abstractmethod
from thinning.interface.IAlgorithm import IAlgorithm
from thinning.DyerRosenfeld import DyerRosenfeld
from thinning.SalariSiy import SalariSiy
from thinning.Kang import Kang
from thinning.Kim import Kim
from thinning.Couprie import Couprie
from thinning.Image import Image


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
