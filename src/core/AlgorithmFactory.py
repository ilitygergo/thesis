import bcolors
from abc import ABC, abstractmethod
from classes.Algorithm import Algorithm
from classes.DyerRosenfeld import DyerRosenfeld
from classes.SalariSiy import SalariSiy
from classes.Kang import Kang
from classes.Kim import Kim
from classes.Couprie import Couprie
from core.Image import Image


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
