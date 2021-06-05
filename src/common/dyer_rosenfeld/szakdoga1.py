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
    def __init__(self, picture_name):
        self.img = get_image_by_name(picture_name)
        self.img_after_step = np.zeros((self.img.shape[0], self.img.shape[1]))
        self.stepCounter = 1


dyer = DyerRosenfeldAlgorithm('test.jpg')

while True:
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

    # Matrixes
    n = dyer.img.shape[0] - 2
    m = dyer.img.shape[1] - 2
    matrix = [0] * n
    for x in range(n):
        matrix[x] = [0] * m

    n = dyer.img.shape[0]
    m = dyer.img.shape[1]
    matrix2 = [0] * n
    for x in range(n):
        matrix2[x] = [' '] * m

    n = dyer.img.shape[0]
    m = dyer.img.shape[1]
    matrix3 = [0] * n
    for x in range(n):
        matrix3[x] = [' '] * m

    print(bcolors.OK, 'Input:', bcolors.ENDC)
    print(bcolors.BOLD, dyer.img, bcolors.ENDC, '\n')
    print('\n')

    # Finding the border points

    for oldal in range(0, 4):
        if oldal == 0:
            print(bcolors.OK, 'North borders:', bcolors.ENDC)
        elif oldal == 1:
            print(bcolors.OK, 'West borders:', bcolors.ENDC)
        elif oldal == 2:
            print(bcolors.OK, 'South borders:', bcolors.ENDC)
        elif oldal == 3:
            print(bcolors.OK, 'East borders:', bcolors.ENDC)
        hatar = 0
        for row in range(1, dyer.img.shape[0] - 1):
            for col in range(1, (dyer.img.shape[1] - 1)):
                a = dyer.img[row - 1, col - 1]
                b = dyer.img[row - 1, col]
                c = dyer.img[row - 1, col + 1]
                d = dyer.img[row, col - 1]
                e = dyer.img[row, col]
                f = dyer.img[row, col + 1]
                g = dyer.img[row + 1, col - 1]
                h = dyer.img[row + 1, col]
                i = dyer.img[row + 1, col + 1]
                grayness = rvalue(b, d, e, f, h) * percent
                if oldal == 0:
                    if b < e - grayness:
                        hatar += 1
                        matrix[row - 1][col - 1] = e
                        matrix2[row][col] = 'X'
                    else:
                        matrix2[row][col] = ' '
                if oldal == 1:
                    if d < e - grayness:
                        hatar += 1
                        matrix[row - 1][col - 1] = e
                        matrix2[row][col] = 'X'
                    else:
                        matrix2[row][col] = ' '
                if oldal == 2:
                    if h < e - grayness:
                        hatar += 1
                        matrix[row - 1][col - 1] = e
                        matrix2[row][col] = 'X'
                    else:
                        matrix2[row][col] = ' '
                if oldal == 3:
                    if f < e - grayness:
                        hatar += 1
                        matrix[row - 1][col - 1] = e
                        matrix2[row][col] = 'X'
                    else:
                        matrix2[row][col] = ' '

        printmatrix(matrix2)
        print('\n')
        print('Összesen:', hatar)

        # Minimize by endpoint and connectedness
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        g = 0
        h = 0
        i = 0
        nem = 0
        igen = 0
        for row in range(1, dyer.img.shape[0] - 1):
            for col in range(1, dyer.img.shape[1] - 1):
                if matrix[row - 1][col - 1] != 0:
                    a = dyer.img[row - 1, col - 1]
                    b = dyer.img[row - 1, col]
                    c = dyer.img[row - 1, col + 1]
                    d = dyer.img[row, col - 1]
                    e = dyer.img[row, col]
                    f = dyer.img[row, col + 1]
                    g = dyer.img[row + 1, col - 1]
                    h = dyer.img[row + 1, col]
                    i = dyer.img[row + 1, col + 1]
                    grayness = rvalue(b, d, e, f, h) * percent
                    if notendpoint(b, d, h, f, e - grayness) and connected(a, b, c, d, e, f, g, h, i, grayness) \
                            and dyer.img[row][col] != 0:
                        igen += 1
                        matrix3[row][col] = 'X'
                    else:
                        nem += 1
                        continue

        for row in range(1, dyer.img.shape[0] - 1):
            for col in range(1, dyer.img.shape[1] - 1):
                b = dyer.img[row - 1, col]
                d = dyer.img[row, col - 1]
                e = dyer.img[row, col]
                f = dyer.img[row, col + 1]
                h = dyer.img[row + 1, col]
                if matrix3[row][col] == 'X':
                    dyer.img[row][col] = minimize(b, d, h, f, e)

        print('Delete:', bcolors.ERR, igen, bcolors.ENDC)
        print('Cannot delete:', bcolors.OK, nem, bcolors.ENDC, '\n')
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
