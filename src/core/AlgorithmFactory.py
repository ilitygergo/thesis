import bcolors
from abc import ABC, abstractmethod
from classes.Algorithm import Algorithm
from classes.DyerRosenfeld import DyerRosenfeld
from classes.SalariSiy import SalariSiy
from classes.Kang import Kang
from classes.Kim import Kim
from classes.Couprie import Couprie


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
