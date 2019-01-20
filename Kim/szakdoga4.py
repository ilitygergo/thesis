import cv2
import bcolors
from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import nearneighbourmin
from Common.functions import farneighbourmin
from Common.functions import equalmatrix
from Common.functions import makeequalmatrix
from Common.functions import countf

print(bcolors.OK, " _  ___             _                  _____ _           _ ")
print(" | |/ (_)           | |                / ____| |         (_)")
print(" | ' / _ _ __ ___   | |     ___  ___  | |    | |__   ___  _ ")
print(" |  < | | '_ ` _ \  | |    / _ \/ _ \ | |    | '_ \ / _ \| |")
print(" | . \| | | | | | | | |___|  __/  __/ | |____| | | | (_) | |")
print(" |_|\_\_|_| |_| |_| |______\___|\___|  \_____|_| |_|\___/|_|", bcolors.ENDC)

# Reading in the image as a gray image
picture = 'chromosomemini'

img = imreadgray('../Common/' + picture + '.png')
img2 = imreadgray('../Common/' + picture + '.png')
comp = imreadgray('../Common/' + picture + '.png')
compstar = imreadgray('../Common/' + picture + '.png')
c8 = imreadgray('../Common/' + picture + '.png')
E = imreadgray('../Common/' + picture + '.png')
R = imreadgray('../Common/' + picture + '.png')
O1 = imreadgray('../Common/' + picture + '.png')
O2 = imreadgray('../Common/' + picture + '.png')

# Converting values 0-255
flip(img)
flip(img2)
flip(comp)
flip(compstar)
flip(c8)
flip(E)
flip(R)
flip(O1)
flip(O2)

# Initialization
h = 100
size = img.shape
for row in range(0, size[0]):
    for col in range(0, size[1]):
        O1[row][col] = 0
        O2[row][col] = 0
        comp[row][col] = 0
        E[row][col] = 0
        R[row][col] = 0
        compstar[row][col] = 0
        c8[row][col] = 0
equal = True
lepes = 1

print(img)

while equal:

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            E[row][col] = nearneighbourmin(comp, row, col)

    # Ridge detection
    for row in range(2, size[0] - 2):
        for col in range(2, size[1] - 2):
            O1[row][col] = nearneighbourmin(img, row, col)
            O2[row][col] = farneighbourmin(img, row, col)

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if (int(img[row][col]) - int(O1[row][col]) > 0) and int(img[row][col]) - int(O2[row][col]) > h:
                R[row][col] = img[row][col]
            else:
                R[row][col] = 0

    # Comp*
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            compstar[row][col] = max(int(E[row][col]), int(R[row][col]))

    # C8 matrix
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            c8[row][col] = countf(comp, row, col)

    # Connectivity restoration
    for row in range(1, size[0] - 1):
        for col in range(2, size[1] - 1):
            if R[row][col] == 0 and c8[row][col] >= 2:
                compstar[row][col] = comp[row][col]

    makeequalmatrix(comp, compstar, size)

    print(bcolors.BLUE, '\n', lepes, '. run:')
    print(comp, '\n', bcolors.ENDC)

    lepes += 1
    if equalmatrix(comp, img2, size):
        break
    else:
        makeequalmatrix(img2, comp, size)

# Converting the values back to normal
flip(comp)

# Saving
cv2.imwrite('results/' + picture + '.png', comp)