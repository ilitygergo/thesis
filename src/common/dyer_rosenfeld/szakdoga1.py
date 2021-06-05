import os
import numpy as np
import cv2
import bcolors
import files.input as pic_folder
from common.functions import printmatrix
from common.functions import rvalue
from common.functions import minimize
from common.functions import imreadgray
from common.functions import notendpoint
from common.functions import flip
from common.functions import connected
from common.functions import equalmatrix
from common.functions import makeequalmatrix

print(bcolors.OK, " _____                    _____                       __     _     _ ")
print(" |  __ \                  |  __ \                     / _|   | |   | |")
print(" | |  | |_   _  ___ _ __  | |__) |___  ___  ___ _ __ | |_ ___| | __| |")
print(" | |  | | | | |/ _ \ '__| |  _  // _ \/ __|/ _ \ '_ \|  _/ _ \ |/ _` |")
print(" | |__| | |_| |  __/ |    | | \ \ (_) \__ \  __/ | | | ||  __/ | (_| |")
print(" |_____/ \__, |\___|_|    |_|  \_\___/|___/\___|_| |_|_| \___|_|\__,_|")
print("          __/ |                                                       ")
print("         |___/                                                        ", bcolors.ENDC)


def get_image_by_name(name):
    return flip(imreadgray(
        f'{os.path.dirname(pic_folder.__file__)}{os.path.sep}{name}'
    ))


class DyerRosenfeldAlgorithm:
    NORTH_BORDER = 0
    WEST_BORDER = 1
    SOUTH_BORDER = 2
    EAST_BORDER = 3
    percent = 0
    grayness = 0
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = 0
    i = 0

    def __init__(self, picture_name):
        self.img = get_image_by_name(picture_name)
        self.img_after_step = np.zeros((self.img.shape[0], self.img.shape[1]))
        self.stepCounter = 1
        self.borderPointCount = 0
        self.deleteCount = 0
        self.cantDeleteCount = 0
        self.matrix = [0] * (self.img.shape[0] - 2)
        for index in range(self.img.shape[0] - 2):
            self.matrix[index] = [0] * (self.img.shape[1] - 2)
        self.matrix2 = [0] * (self.img.shape[0])
        self.matrix3 = [0] * (self.img.shape[0])
        for index in range(self.img.shape[0]):
            self.matrix2[index] = [' '] * (self.img.shape[1])
            self.matrix3[index] = [' '] * (self.img.shape[1])

    def reset_neighbour_points(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.g = 0
        self.h = 0
        self.i = 0

    def init_values(self):
        self.grayness = 0
        self.matrix = [0] * (self.img.shape[0] - 2)
        for index in range(self.img.shape[0] - 2):
            self.matrix[index] = [0] * (self.img.shape[1] - 2)

        self.matrix2 = [0] * (self.img.shape[0])
        self.matrix3 = [0] * (self.img.shape[0])
        for index in range(self.img.shape[0]):
            self.matrix2[index] = [' '] * (self.img.shape[1])
            self.matrix3[index] = [' '] * (self.img.shape[1])

    def find_border_points(self, side):
        self.borderPointCount = 0
        if side == self.NORTH_BORDER:
            print(bcolors.OK, 'North borders:', bcolors.ENDC)
        elif side == self.WEST_BORDER:
            print(bcolors.OK, 'West borders:', bcolors.ENDC)
        elif side == self.SOUTH_BORDER:
            print(bcolors.OK, 'South borders:', bcolors.ENDC)
        elif side == self.EAST_BORDER:
            print(bcolors.OK, 'East borders:', bcolors.ENDC)

        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, (self.img.shape[1] - 1)):
                self.a = self.img[rowIndex - 1, colIndex - 1]
                self.b = self.img[rowIndex - 1, colIndex]
                self.c = self.img[rowIndex - 1, colIndex + 1]
                self.d = self.img[rowIndex, colIndex - 1]
                self.e = self.img[rowIndex, colIndex]
                self.f = self.img[rowIndex, colIndex + 1]
                self.g = self.img[rowIndex + 1, colIndex - 1]
                self.h = self.img[rowIndex + 1, colIndex]
                self.i = self.img[rowIndex + 1, colIndex + 1]
                self.grayness = rvalue(self.b, self.d, self.e, self.f, self.h) * self.percent
                if side == self.NORTH_BORDER:
                    if self.b < self.e - self.grayness:
                        self.borderPointCount += 1
                        self.matrix[rowIndex - 1][colIndex - 1] = self.e
                        self.matrix2[rowIndex][colIndex] = 'X'
                    else:
                        self.matrix2[rowIndex][colIndex] = ' '
                if side == self.WEST_BORDER:
                    if self.d < self.e - self.grayness:
                        self.borderPointCount += 1
                        self.matrix[rowIndex - 1][colIndex - 1] = self.e
                        self.matrix2[rowIndex][colIndex] = 'X'
                    else:
                        self.matrix2[rowIndex][colIndex] = ' '
                if side == self.SOUTH_BORDER:
                    if self.h < self.e - self.grayness:
                        self.borderPointCount += 1
                        self.matrix[rowIndex - 1][colIndex - 1] = self.e
                        self.matrix2[rowIndex][colIndex] = 'X'
                    else:
                        self.matrix2[rowIndex][colIndex] = ' '
                if side == self.EAST_BORDER:
                    if self.f < self.e - self.grayness:
                        self.borderPointCount += 1
                        self.matrix[rowIndex - 1][colIndex - 1] = self.e
                        self.matrix2[rowIndex][colIndex] = 'X'
                    else:
                        self.matrix2[rowIndex][colIndex] = ' '

    def mark_pixels_to_delete(self):
        self.reset_neighbour_points()
        self.cantDeleteCount = 0
        self.deleteCount = 0

        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, self.img.shape[1] - 1):
                if self.matrix[rowIndex - 1][colIndex - 1] != 0:
                    self.a = self.img[rowIndex - 1, colIndex - 1]
                    self.b = self.img[rowIndex - 1, colIndex]
                    self.c = self.img[rowIndex - 1, colIndex + 1]
                    self.d = self.img[rowIndex, colIndex - 1]
                    self.e = self.img[rowIndex, colIndex]
                    self.f = self.img[rowIndex, colIndex + 1]
                    self.g = self.img[rowIndex + 1, colIndex - 1]
                    self.h = self.img[rowIndex + 1, colIndex]
                    self.i = self.img[rowIndex + 1, colIndex + 1]
                    self.grayness = rvalue(self.b, self.d, self.e, self.f, self.h) * self.percent
                    if notendpoint(self.b, self.d, self.h, self.f, self.e - self.grayness) \
                            and connected(self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i, self.grayness) \
                            and self.img[rowIndex][colIndex] != 0:
                        self.deleteCount += 1
                        self.matrix3[rowIndex][colIndex] = 'X'
                    else:
                        self.cantDeleteCount += 1
                        continue


dyer = DyerRosenfeldAlgorithm('shapes.png')

while True:
    dyer.reset_neighbour_points()
    dyer.init_values()
    print(bcolors.OK, 'Input:', bcolors.ENDC)
    print(bcolors.BOLD, dyer.img, bcolors.ENDC, '\n')
    print('\n')

    # Finding the border points
    for sideValue in range(0, 4):
        dyer.find_border_points(sideValue)
        printmatrix(dyer.matrix2)
        print('\n')
        print('Összesen:', dyer.borderPointCount)

        # Minimize by endpoint and connectedness
        dyer.mark_pixels_to_delete()

        for row in range(1, dyer.img.shape[0] - 1):
            for col in range(1, dyer.img.shape[1] - 1):
                b = dyer.img[row - 1, col]
                d = dyer.img[row, col - 1]
                e = dyer.img[row, col]
                f = dyer.img[row, col + 1]
                h = dyer.img[row + 1, col]
                if dyer.matrix3[row][col] == 'X':
                    dyer.img[row][col] = minimize(b, d, h, f, e)

        print('Delete:', bcolors.ERR, dyer.deleteCount, bcolors.ENDC)
        print('Cannot delete:', bcolors.OK, dyer.cantDeleteCount, bcolors.ENDC, '\n')
        print(bcolors.OK, 'Output:', bcolors.ENDC)
        print(bcolors.BOLD, dyer.img, bcolors.ENDC)

    # Making sure that the function runs until the image has no points left to remove
    print(bcolors.BLUE, '\n', dyer.stepCounter, '. run:')
    print(dyer.img, '\n', bcolors.ENDC)

    dyer.stepCounter += 1
    if equalmatrix(dyer.img, dyer.img_after_step, dyer.img.shape):
        break
    else:
        makeequalmatrix(dyer.img_after_step, dyer.img, dyer.img.shape)

# Converting the values back to normal
flip(dyer.img)

# Saving
cv2.imwrite('test.png', dyer.img)
