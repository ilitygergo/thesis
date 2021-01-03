import bcolors
from abc import ABC, abstractmethod
from src.classes.Algorithm import Algorithm
from src.classes.DyerRosenfeld import DyerRosenfeld
from src.classes.SalariSiy import SalariSiy
from src.classes.Kang import Kang
from src.classes.Kim import Kim
from src.classes.Couprie import Couprie


class AlgorithmFactory(ABC):
    @abstractmethod
    def factory(self):
        pass

    def runAlgorithm(self):
        algorithm = self.factory()
        print(bcolors.OK, algorithm.getName(), bcolors.ENDC)


class DyerRosenfeldFactory(AlgorithmFactory):
    def factory(self) -> Algorithm:
        return DyerRosenfeld()


class SalariSiyFactory(AlgorithmFactory):
    def factory(self) -> Algorithm:
        return SalariSiy()


class KangFactory(AlgorithmFactory):
    def factory(self) -> Algorithm:
        return Kang()


class KimFactory(AlgorithmFactory):
    def factory(self) -> Algorithm:
        return Kim()


class CouprieFactory(AlgorithmFactory):
    def factory(self) -> Algorithm:
        return Couprie()
