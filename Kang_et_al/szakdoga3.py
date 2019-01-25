import cv2
import bcolors
from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import localmaximum
from Common.functions import endpoint
from Common.functions import connectedcorner
from Common.functions import connectedpath
from Common.functions import borderpoint
from Common.functions import findroad
from Common.functions import connectedcomponents
from Common.functions import printmatrix

print(bcolors.OK, " _  __                    _____       _       _  ___           ")
print(" | |/ /                   / ____|     | |     | |/ (_)          ")
print(" | ' / __ _ _ __   __ _  | (___  _   _| |__   | ' / _ _ __ ___  ")
print(" |  < / _` | '_ \ / _` |  \___ \| | | | '_ \  |  < | | '_ ` _ \ ")
print(" | . \ (_| | | | | (_| |  ____) | |_| | | | | | . \| | | | | | |")
print(" |_|\_\__,_|_| |_|\__, | |_____/ \__,_|_| |_| |_|\_\_|_| |_| |_|")
print("                   __/ |                                        ")
print("                  |___/                                         ", bcolors.ENDC, '\n')

# Beolvasás szürkeárnyalatos képként
picture = 'sima'

img = imreadgray('../Common/' + picture + '.png')
img2 = imreadgray('../Common/' + picture + '.png')
helper = imreadgray('../Common/' + picture + '.png')
psi = imreadgray('../Common/' + picture + '.png')
psis = imreadgray('../Common/' + picture + '.png')
skeleton = imreadgray('../Common/' + picture + '.png')
matrix = imreadgray('../Common/' + picture + '.png')
matrix2 = imreadgray('../Common/' + picture + '.png')
help = imreadgray('../Common/' + picture + '.png')

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
        helper[row][col] = 0
        img2[row][col] = 0
        psis[row][col] = 0
        matrix[row][col] = 0
        matrix2[row][col] = 0
        help[row][col] = 0

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
        if psi[row][col] == 5:
            helper[row][col] = 5
        if psi[row][col] >= 6:
            skeleton[row][col] = psi[row][col]
            img2[row][col] = img[row][col]

print(bcolors.WARN, 'PSI >= 6', bcolors.ENDC)
print(img2, '\n')
deleted = 0

for x in range(3):
    for row in range(2, size[0] - 2):
        for col in range(2, size[1] - 2):
            if psi[row][col] == 6 + x:
                if borderpoint(img2[row][col + 1], img2[row - 1][col], img2[row][col - 1], img2[row + 1][col]):
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

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if psi[row][col] == 5:
            if img2[row - 1][col] != 0 or img2[row - 1][col - 1] != 0 or img2[row][col - 1] != 0 \
                    or img2[row + 1][col - 1] != 0 or img2[row + 1][col] != 0 or img2[row + 1][col + 1] != 0 \
                    or img2[row][col + 1] != 0 or img2[row - 1][col + 1] != 0:
                matrix[row][col] = 1

matrix2 = connectedcomponents(matrix2, img, size)
print('Skeleton:')
print(img2)

count = True

for row in range(1, size[0] - 1):
    count = True
    for col in range(1, size[1] - 1):
        if img2[row][col] != 0:
            if psi[row - 1][col] == 5:
                findroad(matrix, matrix2, helper, img, img2, row - 1, col, img2[row][col])
                matrix2 = connectedcomponents(matrix2, img, size)
            if psi[row - 1][col - 1] == 5:
                findroad(matrix, matrix2, helper, img, img2, row - 1, col - 1, img2[row][col])
                matrix2 = connectedcomponents(matrix2, img, size)
            if psi[row][col - 1] == 5:
                findroad(matrix, matrix2, helper, img, img2, row, col - 1, img2[row][col])
                matrix2 = connectedcomponents(matrix2, img, size)
            if psi[row + 1][col - 1] == 5:
                findroad(matrix, matrix2, helper, img, img2, row + 1, col - 1, img2[row][col])
                matrix2 = connectedcomponents(matrix2, img, size)
            if psi[row + 1][col] == 5:
                findroad(matrix, matrix2, helper, img, img2, row + 1, col, img2[row][col])
                matrix2 = connectedcomponents(matrix2, img, size)
            if psi[row + 1][col + 1] == 5:
                findroad(matrix, matrix2, helper, img, img2, row + 1, col + 1, img2[row][col])
                matrix2 = connectedcomponents(matrix2, img, size)
            if psi[row][col + 1] == 5:
                findroad(matrix, matrix2, helper, img, img2, row, col + 1, img2[row][col])
                matrix2 = connectedcomponents(matrix2, img, size)
            if psi[row - 1][col + 1] == 5:
                findroad(matrix, matrix2, helper, img, img2, row - 1, col + 1, img2[row][col])
                matrix2 = connectedcomponents(matrix2, img, size)
            if count:
                print(size[0] - 1, '/', row)
                count = False
        elif count:
            print(size[0] - 1, '/', row)
            count = False

print(bcolors.WARN, 'Skeleton after connectivity restoration:', bcolors.ENDC)
print(bcolors.ERR, 'Deleted:', deleted, bcolors.ENDC)
print(img2)

# Converting the values back to normal
flip(img2)

# Saving
cv2.imwrite('results/' + picture + '.png', img2)
