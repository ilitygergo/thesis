import cv2
import time
import bcolors
from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import equalmatrix
from Common.functions import makeequalmatrix
from Common.functions import borderpoint8
from Common.functions import binmatrix
from Common.functions import lowneighbour
from Common.functions import converttoarray
from Common.functions import arraytonum

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
picture = 'dragon'

img = imreadgray('../Common/' + picture + '.png')
img2 = imreadgray('../Common/' + picture + '.png')
helper = imreadgray('../Common/' + picture + '.png')
lowest = imreadgray('../Common/' + picture + '.png')

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
table = []

with open("lookup", "rb") as f:
    byte = f.read(1)
    while byte:
        table.append(int.from_bytes(byte, "little"))
        byte = f.read(1)

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
            binmatrixhelper = converttoarray(binmatrixhelper, 2, 2)
            binmatrixhelper = arraytonum(binmatrixhelper)
            helper[row][col] = table[binmatrixhelper]

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
cv2.imwrite('results_lookup/' + picture + '.png', img)

print("My program took", time.time() - start_time, "to run")
