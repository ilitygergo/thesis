import bcolors

from common.algorithm import Algorithm
from src.common.functions import (
    borderpoint,
    connectedcorner,
    connectedpath,
    countnotzero,
    endpoint,
    equalmatrix,
    get_image_by_name,
    localmaximum,
    makeequalmatrix,
    save_image_by_name,
)


class KangEtAlAlgorithm(Algorithm):
    psi_value = 6

    def __init__(self, img_name):
        self.imgName = img_name
        self.img = get_image_by_name(img_name)
        self.img2 = get_image_by_name(img_name)
        self.helper = get_image_by_name(img_name)
        self.psi = get_image_by_name(img_name)
        self.psis = get_image_by_name(img_name)
        self.skeleton = get_image_by_name(img_name)
        self.matrix = get_image_by_name(img_name)
        self.matrix2 = get_image_by_name(img_name)
        self.help = get_image_by_name(img_name)
        self.borders = get_image_by_name(img_name)

    def initialize(self):  # noqa: C901
        for rowIndex in range(0, self.img.shape[0]):
            for colIndex in range(0, self.img.shape[1]):
                self.psi[rowIndex][colIndex] = 0
                self.skeleton[rowIndex][colIndex] = 0
                self.img2[rowIndex][colIndex] = 0
                self.psis[rowIndex][colIndex] = 0
                self.matrix[rowIndex][colIndex] = 0
                self.matrix2[rowIndex][colIndex] = 0
                self.helper[rowIndex][colIndex] = 0
                self.borders[rowIndex][colIndex] = 0

        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, self.img.shape[1] - 1):
                if self.img[rowIndex][colIndex] != 0:
                    if self.img[rowIndex - 1][colIndex] <= self.img[rowIndex][colIndex]:
                        self.psi[rowIndex][colIndex] += 1
                    if (
                        self.img[rowIndex - 1][colIndex - 1]
                        <= self.img[rowIndex][colIndex]
                    ):
                        self.psi[rowIndex][colIndex] += 1
                    if self.img[rowIndex][colIndex - 1] <= self.img[rowIndex][colIndex]:
                        self.psi[rowIndex][colIndex] += 1
                    if (
                        self.img[rowIndex + 1][colIndex - 1]
                        <= self.img[rowIndex][colIndex]
                    ):
                        self.psi[rowIndex][colIndex] += 1
                    if self.img[rowIndex + 1][colIndex] <= self.img[rowIndex][colIndex]:
                        self.psi[rowIndex][colIndex] += 1
                    if (
                        self.img[rowIndex + 1][colIndex + 1]
                        <= self.img[rowIndex][colIndex]
                    ):
                        self.psi[rowIndex][colIndex] += 1
                    if self.img[rowIndex][colIndex + 1] <= self.img[rowIndex][colIndex]:
                        self.psi[rowIndex][colIndex] += 1
                    if (
                        self.img[rowIndex - 1][colIndex + 1]
                        <= self.img[rowIndex][colIndex]
                    ):
                        self.psi[rowIndex][colIndex] += 1

        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, self.img.shape[1] - 1):
                if self.psi[rowIndex][colIndex] >= self.psi_value:
                    self.skeleton[rowIndex][colIndex] = self.psi[rowIndex][colIndex]
                    self.img2[rowIndex][colIndex] = self.img[rowIndex][colIndex]

        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, self.img.shape[1] - 1):
                self.img[rowIndex][colIndex] = self.img2[rowIndex][colIndex]

    def step(self):  # noqa: C901
        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, self.img.shape[1] - 1):
                if borderpoint(kang.img, rowIndex, colIndex):
                    self.borders[rowIndex][colIndex] = 1

        for rowIndex in range(2, self.img.shape[0] - 2):
            for colIndex in range(2, self.img.shape[1] - 2):
                if self.psi[rowIndex][colIndex] == self.psi_value + x:
                    if self.borders[rowIndex][colIndex] == 1:
                        if localmaximum(
                            self.img2[rowIndex][colIndex],
                            self.img2[rowIndex][colIndex + 1],
                            self.img2[rowIndex - 1][colIndex + 1],
                            self.img2[rowIndex - 1][colIndex],
                            self.img2[rowIndex - 1][colIndex - 1],
                            self.img2[rowIndex][colIndex - 1],
                            self.img2[rowIndex + 1][colIndex - 1],
                            self.img2[rowIndex + 1][colIndex],
                            self.img2[rowIndex + 1][colIndex + 1],
                        ):
                            continue
                        if endpoint(self.img2, rowIndex, colIndex):
                            continue
                        if not connectedcorner(self.img2, rowIndex, colIndex):
                            continue
                        if not connectedpath(self.img2, rowIndex, colIndex):
                            continue
                        self.img2[rowIndex][colIndex] = 0

    def clear_helpers(self):
        pass

    def after_processing(self):
        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, self.img.shape[1] - 1):
                if self.psi[rowIndex][colIndex] == 5:
                    if countnotzero(self.img2, rowIndex, colIndex):
                        self.img2[rowIndex][colIndex] = self.helper[rowIndex][colIndex]

    def print_algorithm_name(self):
        print(
            bcolors.OK,
            r"""
         _  __                    _____       _       _  ___
        | |/ /                   / ____|     | |     | |/ (_)
        | ' / __ _ _ __   __ _  | (___  _   _| |__   | ' / _ _ __ ___
        |  < / _` | '_ \ / _` |  \___ \| | | | '_ \  |  < | | '_ ` _ \
        | . \ (_| | | | | (_| |  ____) | |_| | | | | | . \| | | | | | |
        |_|\_\__,_|_| |_|\__, | |_____/ \__,_|_| |_| |_|\_\_|_| |_| |_|
                          __/ |
                         |___/
        """,
            bcolors.ENDC,
        )


kang = KangEtAlAlgorithm("shapes.png")
kang.print_algorithm_name()
kang.initialize()

for x in range(3):
    while True:
        kang.step()

        if equalmatrix(kang.img, kang.img2, kang.img.shape):
            break
        else:
            makeequalmatrix(kang.img, kang.img2, kang.img.shape)

kang.after_processing()
save_image_by_name(kang.imgName, kang.img2)
