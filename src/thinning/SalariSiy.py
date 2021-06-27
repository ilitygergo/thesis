import bcolors
from src.common.functions import *
from thinning.interface.IAlgorithm import IAlgorithm


class SalariSiy(IAlgorithm):

    def __init__(self, img_name):
        self.imgName = img_name
        self.img = get_image_by_name(img_name)
        self.imgBeforeStep = get_image_by_name(img_name)
        self.g1 = get_image_by_name(img_name)
        self.g2 = get_image_by_name(img_name)
        self.borders = get_image_by_name(img_name)
        self.maximum = 0

    def initialize(self):
        hist = [0] * 256
        maxima = 0

        for rowIndex in range(self.img.shape[0]):
            for colIndex in range(self.img.shape[1]):
                if rowIndex == 0 or colIndex == 0 or rowIndex == self.img.shape[0] or colIndex == self.img.shape[1]:
                    self.img[rowIndex][colIndex] = 0
                self.g1[rowIndex][colIndex] = 0
                self.g2[rowIndex][colIndex] = 0
                self.borders[rowIndex][colIndex] = 0

        for rowIndex in range(self.img.shape[0]):
            for colIndex in range(self.img.shape[1]):
                hist[int(self.img[rowIndex][colIndex])] += 1

        for index in range(256):
            if index == 0:
                continue
            if maxima < hist[index]:
                maxima = hist[index]
                self.maximum = index

        self.pre_transformation_step()

    def pre_transformation_step(self):
        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, self.img.shape[1] - 1):
                a = self.g1[rowIndex - 1][colIndex - 1]
                b = self.g1[rowIndex - 1][colIndex]
                c = self.g1[rowIndex - 1][colIndex + 1]
                d = self.g1[rowIndex][colIndex - 1]
                ave = (int(self.img[rowIndex][colIndex - 1]) + int(self.img[rowIndex][colIndex + 1]) + int(
                    self.img[rowIndex - 1][colIndex]) + int(self.img[rowIndex + 1][colIndex])) / 4
                plus = (int(ave) / self.maximum) ** 2
                if int(self.img[rowIndex][colIndex]) + int(min(a, b, c, d) * plus) > 255:
                    self.g1[rowIndex][colIndex] = 255
                else:
                    self.g1[rowIndex][colIndex] = int(self.img[rowIndex][colIndex]) + int(min(a, b, c, d) * int(plus))

        for rowIndex in reversed(range(1, self.img.shape[0] - 1)):
            for colIndex in reversed(range(1, self.img.shape[1] - 1)):
                a = self.g2[rowIndex + 1][colIndex + 1]
                b = self.g2[rowIndex + 1][colIndex]
                c = self.g2[rowIndex + 1][colIndex - 1]
                d = self.g2[rowIndex][colIndex + 1]
                ave = (int(self.img[rowIndex][colIndex - 1]) + int(self.img[rowIndex][colIndex + 1]) + int(
                    self.img[rowIndex - 1][colIndex]) + int(self.img[rowIndex + 1][colIndex])) / 4
                plus = (ave / self.maximum) ** 2
                if (int(self.img[rowIndex][colIndex]) + int(min(a, b, c, d) * plus)) > 255:
                    self.g2[rowIndex][colIndex] = 255
                else:
                    self.g2[rowIndex][colIndex] = int(self.img[rowIndex][colIndex]) + int(min(a, b, c, d) * plus)

        for rowIndex in range(self.img.shape[0]):
            for colIndex in range(self.img.shape[1]):
                self.img[rowIndex][colIndex] = min(self.g1[rowIndex][colIndex], self.g2[rowIndex][colIndex])

    def step(self):
        hatar = 0
        localmax = 0
        end = 0
        conc = 0
        conp = 0
        torolt = 0

        for row in range(1, self.img.shape[0] - 1):
            for col in range(1, self.img.shape[1] - 1):
                if borderpoint(self.img, row, col):
                    hatar += 1
                    self.borders[row][col] = 1

        for row in range(1, self.img.shape[0] - 1):
            for col in range(1, self.img.shape[1] - 1):
                if self.img[row][col] != 0:
                    if self.borders[row][col] == 1:
                        if localmaximum(self.img[row][col], self.img[row][col + 1], self.img[row - 1][col + 1],
                                        self.img[row - 1][col], self.img[row - 1][col - 1],
                                        self.img[row][col - 1],
                                        self.img[row + 1][col - 1], self.img[row + 1][col],
                                        self.img[row + 1][col + 1]):
                            localmax += 1
                            continue
                        if endpoint(self.img, row, col):
                            end += 1
                            continue
                        if not connectedcorner(self.img, row, col):
                            conc += 1
                            continue
                        if not connectedpath(self.img, row, col):
                            conp += 1
                            continue
                        torolt += 1
                        self.img[row][col] = 0

    def after_processing(self):
        pass

    def print_algorithm_name(self):
        print(bcolors.OK, r"""
          _____       _            _        _____ _
         / ____|     | |          (_)      / ____(_)
        | (___   __ _| | __ _ _ __ _ _____| (___  _ _   _ 
         \___ \ / _` | |/ _` | '__| |______\___ \| | | | |
         ____) | (_| | | (_| | |  | |      ____) | | |_| |
        |_____/ \__,_|_|\__,_|_|  |_|     |_____/|_|\__, |
                                                     __/ |
                                                    |___/
        """, bcolors.ENDC)
