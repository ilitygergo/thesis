import cv2
import bcolors
from src.common.functions import imreadgray
from src.common.functions import flip
from src.common.functions import localmaximum
from src.common.functions import endpoint
from src.common.functions import connectedcorner
from src.common.functions import connectedpath
from src.common.functions import borderpoint
from src.common.functions import equalmatrix
from src.common.functions import makeequalmatrix
from src.common.functions import countnotzero

print(bcolors.OK, " _  __                    _____       _       _  ___           ")
print(" | |/ /                   / ____|     | |     | |/ (_)          ")
print(" | ' / __ _ _ __   __ _  | (___  _   _| |__   | ' / _ _ __ ___  ")
print(" |  < / _` | '_ \ / _` |  \___ \| | | | '_ \  |  < | | '_ ` _ \ ")
print(" | . \ (_| | | | | (_| |  ____) | |_| | | | | | . \| | | | | | |")
print(" |_|\_\__,_|_| |_|\__, | |_____/ \__,_|_| |_| |_|\_\_|_| |_| |_|")
print("                   __/ |                                        ")
print("                  |___/                                         ", bcolors.ENDC, '\n')

# Beolvasás szürkeárnyalatos képként
picture = 'text'

img = imreadgray('../common/files/input/' + picture + '.png')
img2 = imreadgray('../common/files/input/' + picture + '.png')
helper = imreadgray('../common/files/input/' + picture + '.png')
psi = imreadgray('../common/files/input/' + picture + '.png')
psis = imreadgray('../common/files/input/' + picture + '.png')
skeleton = imreadgray('../common/files/input/' + picture + '.png')
matrix = imreadgray('../common/files/input/' + picture + '.png')
matrix2 = imreadgray('../common/files/input/' + picture + '.png')
help = imreadgray('../common/files/input/' + picture + '.png')
borders = imreadgray('../common/files/input/' + picture + '.png')

# Értékek átkonvertálása 0-255
flip(psis)
flip(img)
flip(img2)
flip(helper)
flip(psi)
flip(skeleton)

# Initialization
size = img.shape
psivalue = 6
xrp = 0
f = 0

for row in range(0, size[0]):
    for col in range(0, size[1]):
        psi[row][col] = 0
        skeleton[row][col] = 0
        img2[row][col] = 0
        psis[row][col] = 0
        matrix[row][col] = 0
        matrix2[row][col] = 0
        help[row][col] = 0
        borders[row][col] = 0

print(bcolors.WARN, 'Original grayscale image', bcolors.ENDC)
print(img, '\n')

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if img[row][col] != 0:
            if img[row - 1][col] <= img[row][col]:
                psi[row][col] += 1
            if img[row - 1][col - 1] <= img[row][col]:
                psi[row][col] += 1
            if img[row][col - 1] <= img[row][col]:
                psi[row][col] += 1
            if img[row + 1][col - 1] <= img[row][col]:
                psi[row][col] += 1
            if img[row + 1][col] <= img[row][col]:
                psi[row][col] += 1
            if img[row + 1][col + 1] <= img[row][col]:
                psi[row][col] += 1
            if img[row][col + 1] <= img[row][col]:
                psi[row][col] += 1
            if img[row - 1][col + 1] <= img[row][col]:
                psi[row][col] += 1

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if psi[row][col] >= 6:
            skeleton[row][col] = psi[row][col]
            img2[row][col] = img[row][col]

print(bcolors.WARN, 'PSI >= 6', bcolors.ENDC)
print(img2, '\n')

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        img[row][col] = img2[row][col]
deleted = 0
change = True

for x in range(3):

    while change:

        for row in range(1, size[0] - 1):
            for col in range(1, size[1] - 1):
                if borderpoint(img, row, col):
                    borders[row][col] = 1

        for row in range(2, size[0] - 2):
            for col in range(2, size[1] - 2):
                if psi[row][col] == 6 + x:
                    if borders[row][col] == 1:
                        if localmaximum(img2[row][col], img2[row][col + 1], img2[row - 1][col + 1],
                                         img2[row - 1][col], img2[row - 1][col - 1], img2[row][col - 1],
                                         img2[row + 1][col - 1], img2[row + 1][col], img2[row + 1][col + 1]):
                            continue
                        if endpoint(img2, row, col):
                            continue
                        if not connectedcorner(img2, row, col):
                            continue
                        if not connectedpath(img2, row, col):
                            continue
                        deleted += 1
                        img2[row][col] = 0
        if equalmatrix(img, img2, size):
            break
        else:
            makeequalmatrix(img, img2, size)

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if psi[row][col] == 5:
            if countnotzero(img2, row, col):
                img2[row][col] = helper[row][col]

print(bcolors.WARN, 'Skeleton after connectivity restoration:', bcolors.ENDC)
print(bcolors.ERR, 'Deleted:', deleted, bcolors.ENDC)
print(img2)

# Converting the values back to normal
flip(img2)

# Saving
cv2.imwrite('results/' + picture + '.png', img2)
