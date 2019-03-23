import cv2
import bcolors
from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import equalmatrix
from Common.functions import makeequalmatrix
from Common.functions import oneobject
from Common.functions import borderpoint8
from Common.functions import simpleafterremove
from Common.functions import forbidden
from Common.functions import endpointmodified
from Common.functions import binmatrix

print(bcolors.OK, "  _____                       _             _           _ ")
print("  / ____|                     (_)           | |         | |")
print(" | |     ___  _   _ _ __  _ __ _  ___    ___| |_    __ _| |")
print(" | |    / _ \| | | | '_ \| '__| |/ _ \  / _ \ __|  / _` | |")
print(" | |___| (_) | |_| | |_) | |  | |  __/ |  __/ |_  | (_| | |")
print("  \_____\___/ \__,_| .__/|_|  |_|\___|  \___|\__|  \__,_|_|")
print("                   | |                                     ")
print("                   |_|                                     ", bcolors.ENDC)

# Reading in the pictures as a gray picture
picture = '1'

img = imreadgray('../Common/' + picture + '.png')
img2 = imreadgray('../Common/' + picture + '.png')
helper = imreadgray('../Common/' + picture + '.png')

# Converting values 0-255
img = flip(img)
img2 = flip(img2)
helper = flip(helper)

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

    for row in range(2, size[0] - 2):
        for col in range(2, size[1] - 2):
            if img[row][col] == 0:
                continue
            if borderpoint8(img, row, col):
                border[row][col] = 'X'

    for row in range(2, size[0] - 2):
        for col in range(2, size[1] - 2):
            binmatrixhelper = binmatrix(img, row, col)
            print(binmatrixhelper)
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
                img[row][col] = 0

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
