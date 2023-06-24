import bcolors

from common.algorithm import Algorithm
from src.common.functions import (
    arraytonum,
    binmatrix,
    borderpoint8,
    converttoarray,
    endpointmodified,
    equalmatrix,
    forbidden,
    get_image_by_name,
    lowneighbour,
    makeequalmatrix,
    oneobject,
    save_image_by_name,
    simpleafterremove,
)


class CouprieEtAlAlgorithm(Algorithm):
    binmatrixhelper = 0

    def __init__(self, img_name, lookup=False):
        self.imgName = img_name
        self.lookup = lookup
        self.img = get_image_by_name(img_name)
        self.img2 = get_image_by_name(img_name)
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

    def step(self):  # noqa: C901
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
                CouprieEtAlAlgorithm.binmatrixhelper = binmatrix(
                    self.img, rowIndex, colIndex, self.img.shape
                )
                if self.border[rowIndex][colIndex] == "O":
                    continue

                if self.lookup:
                    CouprieEtAlAlgorithm.binmatrixhelper = converttoarray(
                        CouprieEtAlAlgorithm.binmatrixhelper, 2, 2
                    )
                    CouprieEtAlAlgorithm.binmatrixhelper = arraytonum(
                        CouprieEtAlAlgorithm.binmatrixhelper
                    )
                    self.helper[rowIndex][colIndex] = self.table[
                        CouprieEtAlAlgorithm.binmatrixhelper
                    ]
                else:
                    if endpointmodified(CouprieEtAlAlgorithm.binmatrixhelper, 2, 2):
                        continue
                    if not oneobject(CouprieEtAlAlgorithm.binmatrixhelper, 2, 2) <= 1:
                        continue
                    if not simpleafterremove(
                        CouprieEtAlAlgorithm.binmatrixhelper, 2, 2
                    ):
                        continue
                    if forbidden(CouprieEtAlAlgorithm.binmatrixhelper, 2, 2):
                        continue
                    self.helper[rowIndex][colIndex] = 1

        for row in range(0, self.img.shape[0]):
            for col in range(0, self.img.shape[1]):
                if self.helper[row][col] == 1:
                    self.img[row][col] = self.lowest[row][col]

        makeequalmatrix(self.helper, self.img, self.img.shape)

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


couprie = CouprieEtAlAlgorithm("shapes.png")
couprie.initialize()

while True:
    couprie.step()

    if equalmatrix(couprie.img, couprie.img2, couprie.img.shape):
        break
    else:
        makeequalmatrix(couprie.img2, couprie.img, couprie.img.shape)

save_image_by_name(couprie.imgName, couprie.img)
