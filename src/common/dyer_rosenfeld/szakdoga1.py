import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import cv2
import bcolors
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

# Reading in the pictures as a gray picture
picture = 'text'

img = imreadgray('src/files/input/' + picture + '.png')
img2 = imreadgray('src/files/input/' + picture + '.png')

# Converting values 0-255
img = flip(img)

# Counter and initialization
stepCount = 1
size = img.shape
nemegyenlo = True
for row in range(0, size[0]):
    for col in range(0, size[1]):
        img2[row][col] = 0

while nemegyenlo:

    # Initialization that occurs continuously
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
    n = size[0]-2
    m = size[1]-2
    matrix = [0] * n
    for x in range(n):
        matrix[x] = [0] * m

    n = size[0]
    m = size[1]
    matrix2 = [0] * n
    for x in range(n):
        matrix2[x] = [' '] * m

    n = size[0]
    m = size[1]
    matrix3 = [0] * n
    for x in range(n):
        matrix3[x] = [' '] * m

    print(bcolors.OK, 'Input:', bcolors.ENDC)
    print(bcolors.BOLD, img, bcolors.ENDC,  '\n')
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
        for row in range(1, size[0] - 1):
            for col in range(1, (size[1] - 1)):
                a = img[row - 1, col - 1]
                b = img[row - 1, col]
                c = img[row - 1, col + 1]
                d = img[row, col - 1]
                e = img[row, col]
                f = img[row, col + 1]
                g = img[row + 1, col - 1]
                h = img[row + 1, col]
                i = img[row + 1, col + 1]
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
        for row in range(1, size[0] - 1):
            for col in range(1, size[1] - 1):
                if matrix[row - 1][col - 1] != 0:
                    a = img[row - 1, col - 1]
                    b = img[row - 1, col]
                    c = img[row - 1, col + 1]
                    d = img[row, col - 1]
                    e = img[row, col]
                    f = img[row, col + 1]
                    g = img[row + 1, col - 1]
                    h = img[row + 1, col]
                    i = img[row + 1, col + 1]
                    grayness = rvalue(b, d, e, f, h) * percent
                    # print(img[row][col])
                    if notendpoint(b, d, h, f, e - grayness) and connected(a, b, c, d, e, f, g, h, i, grayness)\
                            and img[row][col] != 0:
                        # print(row, col, ' - ', img[row][col])
                        igen += 1
                        matrix3[row][col] = 'X'
                        # img[row][col] = minimize(b, d, h, f, e)
                    else:
                        nem += 1
                        continue

        for row in range(1, size[0] - 1):
            for col in range(1, size[1] - 1):
                b = img[row - 1, col]
                d = img[row, col - 1]
                e = img[row, col]
                f = img[row, col + 1]
                h = img[row + 1, col]
                if matrix3[row][col] == 'X':
                    img[row][col] = minimize(b, d, h, f, e)

        print('Delete:', bcolors.ERR, igen, bcolors.ENDC)
        print('Cannot delete:', bcolors.OK, nem, bcolors.ENDC, '\n')
        print(bcolors.OK, 'Output:', bcolors.ENDC)
        print(bcolors.BOLD, img, bcolors.ENDC)

    # Making sure that the function runs until the image has no points left to remove
    print(bcolors.BLUE, '\n', lepes, '. run:')
    print(img, '\n', bcolors.ENDC)

    stepCount += 1
    if equalmatrix(img, img2, size):
        break
    else:
        makeequalmatrix(img2, img, size)

# Converting the values back to normal
flip(img)

# Saving
cv2.imwrite(picture + '.png', img)
