import numpy as np
import bcolors
from collections import deque
from common.functions import *

print(bcolors.OK, r"""
  _____                    _____                       __     _     _ 
 |  __ \                  |  __ \                     / _|   | |   | |
 | |  | |_   _  ___ _ __  | |__) |___  ___  ___ _ __ | |_ ___| | __| |
 | |  | | | | |/ _ \ '__| |  _  // _ \/ __|/ _ \ '_ \|  _/ _ \ |/ _` |
 | |__| | |_| |  __/ |    | | \ \ (_) \__ \  __/ | | | ||  __/ | (_| |
 |_____/ \__, |\___|_|    |_|  \_\___/|___/\___|_| |_|_| \___|_|\__,_|
          __/ |                                                       
         |___/                                                        
    """, bcolors.ENDC)


class DyerRosenfeldAlgorithm:
    NORTH_BORDER = 0
    WEST_BORDER = 1
    SOUTH_BORDER = 2
    EAST_BORDER = 3
    percent = 0

    def __init__(self, picture_name):
        self.img = get_image_by_name(picture_name)
        self.imgBeforeStep = np.zeros((self.img.shape[0], self.img.shape[1]))
        self.borderPointPixels = deque()
        self.pixelsToBeDeletedQueue = deque()

    def clear_helpers(self):
        self.borderPointPixels.clear()
        self.pixelsToBeDeletedQueue.clear()

    def step(self):
        for sideValue in range(0, 4):
            self.find_border_points(sideValue)
            self.mark_pixels_to_delete()
            self.minimize_marked_points()

    def find_border_points(self, side):
        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, (self.img.shape[1] - 1)):
                b = self.img[rowIndex - 1, colIndex]
                d = self.img[rowIndex, colIndex - 1]
                e = self.img[rowIndex, colIndex]
                f = self.img[rowIndex, colIndex + 1]
                h = self.img[rowIndex + 1, colIndex]
                grayness = rvalue(b, d, e, f, h) * self.percent
                if side == self.NORTH_BORDER and b < e - grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])
                if side == self.WEST_BORDER and d < e - grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])
                if side == self.SOUTH_BORDER and h < e - grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])
                if side == self.EAST_BORDER and f < e - grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])

    def mark_pixels_to_delete(self):
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
            grayness = rvalue(b, d, e, f, h) * self.percent

            if not notendpoint(b, d, h, f, e - grayness) or not connected(a, b, c, d, e, f, g, h, i, grayness):
                continue
            else:
                self.pixelsToBeDeletedQueue.append([rowIndex, colIndex])

    def minimize_marked_points(self):
        for row, col in self.pixelsToBeDeletedQueue:
            b = self.img[row - 1, col]
            d = self.img[row, col - 1]
            e = self.img[row, col]
            f = self.img[row, col + 1]
            h = self.img[row + 1, col]
            self.img[row][col] = minimize(b, d, h, f, e)


dyer = DyerRosenfeldAlgorithm('shapes.png')

while True:
    print(bcolors.BOLD, dyer.img, bcolors.ENDC, '\n')
    dyer.step()
    dyer.clear_helpers()

    if equalmatrix(dyer.img, dyer.imgBeforeStep, dyer.img.shape):
        break
    else:
        makeequalmatrix(dyer.imgBeforeStep, dyer.img, dyer.img.shape)

flip(dyer.img)
cv2.imwrite('test.png', dyer.img)
