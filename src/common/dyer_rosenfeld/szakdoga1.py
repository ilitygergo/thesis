import os
import numpy as np
import bcolors
import files.input as pic_folder
from collections import deque
from common.functions import *

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
        self.borderPointPixels = deque()
        self.pixelsToBeDeletedQueue = deque()
        self.stepCounter = 1
        self.cantDeleteCount = 0

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
        self.borderPointPixels.clear()
        self.pixelsToBeDeletedQueue.clear()

    def find_border_points(self, side):
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
                        self.borderPointPixels.append([rowIndex, colIndex, self.e])
                if side == self.WEST_BORDER:
                    if self.d < self.e - self.grayness:
                        self.borderPointPixels.append([rowIndex, colIndex, self.e])
                if side == self.SOUTH_BORDER:
                    if self.h < self.e - self.grayness:
                        self.borderPointPixels.append([rowIndex, colIndex, self.e])
                if side == self.EAST_BORDER:
                    if self.f < self.e - self.grayness:
                        self.borderPointPixels.append([rowIndex, colIndex, self.e])

    def mark_pixels_to_delete(self):
        self.reset_neighbour_points()
        self.cantDeleteCount = 0

        for rowIndex, colIndex, value in self.borderPointPixels:
            a = self.img[rowIndex - 1, colIndex - 1]
            b = self.img[rowIndex - 1, colIndex]
            c = self.img[rowIndex - 1, colIndex + 1]
            d = self.img[rowIndex, colIndex - 1]
            e = self.img[rowIndex, colIndex]
            f = self.img[rowIndex, colIndex + 1]
            g = self.img[rowIndex + 1, colIndex - 1]
            h = self.img[rowIndex + 1, colIndex]
            i = self.img[rowIndex + 1, colIndex + 1]
            self.grayness = rvalue(b, d, e, f, h) * self.percent

            if notendpoint(b, d, h, f, e - self.grayness) \
                    and connected(a, b, c, d, e, f, g, h, i, self.grayness):
                self.pixelsToBeDeletedQueue.append([rowIndex, colIndex])
            else:
                self.cantDeleteCount += 1
                continue

    def minimize_marked_points(self):
        deleteCount = len(self.pixelsToBeDeletedQueue)
        for row, col in self.pixelsToBeDeletedQueue:
            b = self.img[row - 1, col]
            d = self.img[row, col - 1]
            e = self.img[row, col]
            f = self.img[row, col + 1]
            h = self.img[row + 1, col]
            self.img[row][col] = minimize(b, d, h, f, e)

        print('Delete:', bcolors.ERR, deleteCount, bcolors.ENDC)
        print('Cannot delete:', bcolors.OK, self.cantDeleteCount, bcolors.ENDC, '\n')
        print(bcolors.OK, 'Output:', bcolors.ENDC)
        print(bcolors.BOLD, self.img, bcolors.ENDC)


dyer = DyerRosenfeldAlgorithm('shapes.png')

while True:
    print(bcolors.BOLD, dyer.img, bcolors.ENDC, '\n')

    dyer.reset_neighbour_points()
    dyer.init_values()

    # Finding the border points
    for sideValue in range(0, 4):
        dyer.find_border_points(sideValue)

        print('\n')
        print('Összesen:', len(dyer.borderPointPixels))

        # Minimize by endpoint and connectedness
        dyer.mark_pixels_to_delete()
        dyer.minimize_marked_points()

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
