import bcolors

from src.common.functions import *
from src.thinning.interface.algorithm_interface import IAlgorithm


class Couprie(IAlgorithm):
    binmatrixhelper = 0

    def __init__(self, img_name, lookup=False):
        self.imgName = img_name
        self.lookup = lookup
        self.img = get_image_by_name(img_name)
        self.imgBeforeStep = get_image_by_name(img_name)
        self.helper = get_image_by_name(img_name)
        self.lowest = get_image_by_name(img_name)
        self.border = None
        self.table = []

    def initialize(self):
        n = self.img.shape[0]
        m = self.img.shape[1]
        self.border = [0] * n
        for x in range(n):
            self.border[x] = ["O"] * m

        with open("lookup", "rb") as f:
            byte = f.read(1)
            while byte:
                self.table.append(int.from_bytes(byte, "little"))
                byte = f.read(1)

    def step(self):
        for rowIndex in range(0, self.img.shape[0]):
            for colIndex in range(0, self.img.shape[1]):
                self.border[rowIndex][colIndex] = "O"
                self.lowest[rowIndex][colIndex] = 0

        for rowIndex in range(2, self.img.shape[0] - 2):
            for colIndex in range(2, self.img.shape[1] - 2):
                if self.img[rowIndex][colIndex] == 0:
                    continue
                if borderpoint8(self.img, rowIndex, colIndex):
                    self.lowest[rowIndex][colIndex] = lowneighbour(
                        self.img, rowIndex, colIndex
                    )
                    self.border[rowIndex][colIndex] = "X"

        for rowIndex in range(2, self.img.shape[0] - 2):
            for colIndex in range(2, self.img.shape[1] - 2):
                Couprie.binmatrixhelper = binmatrix(
                    self.img, rowIndex, colIndex, self.img.shape
                )
                if self.border[rowIndex][colIndex] == "O":
                    continue

                if self.lookup:
                    Couprie.binmatrixhelper = converttoarray(
                        Couprie.binmatrixhelper, 2, 2
                    )
                    Couprie.binmatrixhelper = arraytonum(Couprie.binmatrixhelper)
                    self.helper[rowIndex][colIndex] = self.table[
                        Couprie.binmatrixhelper
                    ]
                else:
                    if endpointmodified(Couprie.binmatrixhelper, 2, 2):
                        continue
                    if not oneobject(Couprie.binmatrixhelper, 2, 2) <= 1:
                        continue
                    if not simpleafterremove(Couprie.binmatrixhelper, 2, 2):
                        continue
                    if forbidden(Couprie.binmatrixhelper, 2, 2):
                        continue
                    self.helper[rowIndex][colIndex] = 1

        for row in range(0, self.img.shape[0]):
            for col in range(0, self.img.shape[1]):
                if self.helper[row][col] == 1:
                    self.img[row][col] = self.lowest[row][col]

        makeequalmatrix(self.helper, self.img, self.img.shape)

    def after_processing(self):
        pass

    def clear_helpers(self):
        pass

    def print_algorithm_name(self):
        print(
            bcolors.OK,
            r"""
          _____                       _             _           _
         / ____|                     (_)           | |         | |
        | |     ___  _   _ _ __  _ __ _  ___    ___| |_    __ _| |
        | |    / _ \| | | | '_ \| '__| |/ _ \  / _ \ __|  / _` | |
        | |___| (_) | |_| | |_) | |  | |  __/ |  __/ |_  | (_| | |
         \_____\___/ \__,_| .__/|_|  |_|\___|  \___|\__|  \__,_|_|
                          | |
                          |_|
        """,
            bcolors.ENDC,
        )
