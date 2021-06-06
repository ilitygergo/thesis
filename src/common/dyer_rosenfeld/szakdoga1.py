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

    def __init__(self, picture_name):
        self.img = get_image_by_name(picture_name)
        self.img_after_step = np.zeros((self.img.shape[0], self.img.shape[1]))
        self.borderPointPixels = deque()
        self.pixelsToBeDeletedQueue = deque()
        self.stepCounter = 1
        self.cantDeleteCount = 0

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
                b = self.img[rowIndex - 1, colIndex]
                d = self.img[rowIndex, colIndex - 1]
                e = self.img[rowIndex, colIndex]
                f = self.img[rowIndex, colIndex + 1]
                h = self.img[rowIndex + 1, colIndex]
                self.grayness = rvalue(b, d, e, f, h) * self.percent
                if side == self.NORTH_BORDER and b < e - self.grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])
                if side == self.WEST_BORDER and d < e - self.grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])
                if side == self.SOUTH_BORDER and h < e - self.grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])
                if side == self.EAST_BORDER and f < e - self.grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])

    def mark_pixels_to_delete(self):
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

flip(dyer.img)
cv2.imwrite('test.png', dyer.img)
