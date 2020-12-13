import cv2
import time
import bcolors
from src.common.functions import imreadgray
from src.common.functions import flip
from src.common.functions import equalmatrix
from src.common.functions import makeequalmatrix
from src.common.functions import borderpoint8
from src.common.functions import binmatrix
from src.common.functions import lowneighbour
from src.common.functions import endpointmodified
from src.common.functions import oneobject
from src.common.functions import forbidden
from src.common.functions import simpleafterremove

start_time = time.time()
print(bcolors.OK, "  _____                       _             _           _ ")
print("  / ____|                     (_)           | |         | |")
print(" | |     ___  _   _ _ __  _ __ _  ___    ___| |_    __ _| |")
print(" | |    / _ \| | | | '_ \| '__| |/ _ \  / _ \ __|  / _` | |")
print(" | |___| (_) | |_| | |_) | |  | |  __/ |  __/ |_  | (_| | |")
print("  \_____\___/ \__,_| .__/|_|  |_|\___|  \___|\__|  \__,_|_|")
print("                   | |                                     ")
print("                   |_|                                     ", bcolors.ENDC)

# Reading in the pictures as a gray picture
picture = 'text'

img = imreadgray('../common/files/input/' + picture + '.png')
img2 = imreadgray('../common/files/input/' + picture + '.png')
helper = imreadgray('../common/files/input/' + picture + '.png')
lowest = imreadgray('../common/files/input/' + picture + '.png')

# Converting values 0-255
img = flip(img)
img2 = flip(img2)
helper = flip(helper)
lowest = flip(lowest)

# Initialization
lepes = 0
size = img.shape
n = size[0]
m = size[1]
border = [0] * n
for x in range(n):
    border[x] = ['O'] * m
binmatrixhelper = 0
print(img, '\n')

while True:
    for row in range(0, size[0]):
        for col in range(0, size[1]):
            border[row][col] = 'O'
            lowest[row][col] = 0

    for row in range(2, size[0] - 2):
        for col in range(2, size[1] - 2):
            if img[row][col] == 0:
                continue
            if borderpoint8(img, row, col):
                lowest[row][col] = lowneighbour(img, row, col)
                border[row][col] = 'X'

    for row in range(2, size[0] - 2):
        for col in range(2, size[1] - 2):
            binmatrixhelper = binmatrix(img, row, col, size)
            if border[row][col] == 'O':
                continue
            if endpointmodified(binmatrixhelper, 2, 2):
                continue
            if not oneobject(binmatrixhelper, 2, 2) <= 1:
                continue
            if not simpleafterremove(binmatrixhelper, 2, 2):
                continue
            if forbidden(binmatrixhelper, 2, 2):
                continue
            helper[row][col] = 1

    for row in range(0, size[0]):
        for col in range(0, size[1]):
            if helper[row][col] == 1:
                img[row][col] = lowest[row][col]

    makeequalmatrix(helper, img, size)

    lepes += 1
    if equalmatrix(img, img2, size):
        break
    else:
        makeequalmatrix(img2, img, size)
        print(bcolors.BLUE, '\n', lepes, '. run:')
        print(img, '\n', bcolors.ENDC)

# Converting the values back to normal
flip(img)

# Saving
cv2.imwrite('results/' + picture + '.png', img)

print("My program took", time.time() - start_time, "to run")
