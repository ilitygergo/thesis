import tkinter as tk
from abc import ABC, abstractmethod

from src.common.functions import (equalmatrix, makeequalmatrix,
                                  save_image_by_name)
from src.thinning.Couprie import Couprie
from src.thinning.DyerRosenfeld import DyerRosenfeld
from src.thinning.Image import Image
from src.thinning.interface.IAlgorithm import IAlgorithm
from src.thinning.Kang import Kang
from src.thinning.Kim import Kim
from src.thinning.SalariSiy import SalariSiy


class AlgorithmFactory(ABC):
    @abstractmethod
    def factory(self, img_name):
        pass

    def runAlgorithm(self, loading_screen: tk.Tk):
        img = Image.getInstance()
        algorithm = self.factory(img.name)
        algorithm.initialize()

        while True:
            loading_screen.update()
            algorithm.step()

            if equalmatrix(algorithm.img, algorithm.imgBeforeStep, algorithm.img.shape):
                break
            else:
                makeequalmatrix(algorithm.imgBeforeStep, algorithm.img, algorithm.img.shape)

        algorithm.after_processing()
        save_image_by_name(algorithm.imgName, algorithm.img)


class DyerRosenfeldFactory(AlgorithmFactory):
    def factory(self, img_name) -> IAlgorithm:
        return DyerRosenfeld(img_name)


class SalariSiyFactory(AlgorithmFactory):
    def factory(self, img_name) -> IAlgorithm:
        return SalariSiy(img_name)


class KangFactory(AlgorithmFactory):
    def factory(self, img_name) -> IAlgorithm:
        return Kang(img_name)


class KimFactory(AlgorithmFactory):
    def factory(self, img_name) -> IAlgorithm:
        return Kim(img_name)


class CouprieFactory(AlgorithmFactory):
    def factory(self, img_name) -> IAlgorithm:
        return Couprie(img_name)
