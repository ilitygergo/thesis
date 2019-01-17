import cv2
import bcolors
from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import notendpoint
from Common.functions import connected

print(bcolors.OK, " _  __                    _____       _       _  ___           ")
print(" | |/ /                   / ____|     | |     | |/ (_)          ")
print(" | ' / __ _ _ __   __ _  | (___  _   _| |__   | ' / _ _ __ ___  ")
print(" |  < / _` | '_ \ / _` |  \___ \| | | | '_ \  |  < | | '_ ` _ \ ")
print(" | . \ (_| | | | | (_| |  ____) | |_| | | | | | . \| | | | | | |")
print(" |_|\_\__,_|_| |_|\__, | |_____/ \__,_|_| |_| |_|\_\_|_| |_| |_|")
print("                   __/ |                                        ")
print("                  |___/                                         ", bcolors.ENDC, '\n')

# Beolvasás szürkeárnyalatos képként
picture = 'fingerprintmini'

img = imreadgray('../Common/' + picture + '.png')
img2 = imreadgray('../Common/' + picture + '.png')
helper = imreadgray('../Common/' + picture + '.png')
psi = imreadgray('../Common/' + picture + '.png')
skeleton = imreadgray('../Common/' + picture + '.png')

# Értékek átkonvertálása 0-255
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

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        psi[row][col] = 0
        skeleton[row][col] = 0
        helper[row][col] = 0
        img2[row][col] = 0

print(bcolors.WARN, 'Original grayscale image', bcolors.ENDC)
print(img, '\n')

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if img[row][col] != 0:
            if int(img[row - 1][col]) <= int(img[row][col]) and int(img[row - 1][col]) != 0:
                psi[row][col] += 1
            if int(img[row - 1][col - 1]) <= int(img[row][col]) and int(img[row - 1][col - 1]) != 0:
                psi[row][col] += 1
            if int(img[row][col - 1]) <= int(img[row][col]) and int(img[row][col - 1]) != 0:
                psi[row][col] += 1
            if int(img[row + 1][col - 1]) <= int(img[row][col]) and int(img[row + 1][col - 1]) != 0:
                psi[row][col] += 1
            if int(img[row + 1][col]) <= int(img[row][col]) and int(img[row + 1][col]) != 0:
                psi[row][col] += 1
            if int(img[row + 1][col + 1]) <= int(img[row][col]) and int(img[row + 1][col + 1]) != 0:
                psi[row][col] += 1
            if int(img[row][col + 1]) <= int(img[row][col]) and int(img[row][col + 1]) != 0:
                psi[row][col] += 1
            if int(img[row - 1][col + 1]) <= int(img[row][col]) and int(img[row - 1][col + 1]) != 0:
                psi[row][col] += 1

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if psi[row][col] == 6:
            helper[row][col] = 5
        if psi[row][col] >= 6:
            skeleton[row][col] = psi[row][col]
            img2[row][col] = img[row][col]

print(bcolors.WARN, 'PSI >= 6', bcolors.ENDC)
print(img2, '\n')
deleted = 0

for i in range(3):
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if psi[row][col] == 6 + i:
                a = img2[row - 1, col - 1]
                b = img2[row - 1, col]
                c = img2[row - 1, col + 1]
                d = img2[row, col - 1]
                e = img2[row, col]
                f = img2[row, col + 1]
                g = img2[row + 1, col - 1]
                h = img2[row + 1, col]
                j = img2[row + 1, col + 1]
                if notendpoint(b, d, h, f, e) and connected(a, b, c, d, e, f, g, h, j, 0):
                    deleted += 1
                    img2[row][col] = 0

print(bcolors.WARN, 'Initial skeleton', bcolors.ENDC)
print(bcolors.ERR, 'Deleted:', deleted, bcolors.ENDC)
print(img2)

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if psi[row][col] == 5 and (img2[row + 1][col] >= 100 or img2[row - 1][col] >= 100 or img2[row][col + 1] >= 100 or img2[row][col - 1] >= 100):
            img2[row][col] = img[row][col]

print(img2)

# Converting the values back to normal
flip(img2)

# Saving
cv2.imwrite('results/' + picture + '.png', img2)
