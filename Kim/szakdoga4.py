import cv2
import bcolors
from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import erosion
from Common.functions import dilation
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
picture = 'sima'

img2 = imreadgray('../Common/' + picture + '.png')
comp = imreadgray('../Common/' + picture + '.png')
compstar = imreadgray('../Common/' + picture + '.png')
c8 = imreadgray('../Common/' + picture + '.png')
E = imreadgray('../Common/' + picture + '.png')
R = imreadgray('../Common/' + picture + '.png')
O1 = imreadgray('../Common/' + picture + '.png')
O2 = imreadgray('../Common/' + picture + '.png')
helper1 = imreadgray('../Common/' + picture + '.png')
helper2 = imreadgray('../Common/' + picture + '.png')
helper3 = imreadgray('../Common/' + picture + '.png')
helper4 = imreadgray('../Common/' + picture + '.png')

# Converting values 0-255
flip(img2)
flip(comp)
flip(compstar)
flip(c8)
flip(E)
flip(R)
flip(O1)
flip(O2)

# Initialization
h = 30
size = comp.shape
for row in range(0, size[0]):
    for col in range(0, size[1]):
        compstar[row][col] = 0
        c8[row][col] = 0
        E[row][col] = 0
        R[row][col] = 0
        O1[row][col] = 0
        O2[row][col] = 0
        helper1[row][col] = 0
        helper2[row][col] = 0
        helper3[row][col] = 0
        helper4[row][col] = 0

equal = True
lepes = 1

print('Comp:')
print(comp)

while equal:

    # Erosion
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            E[row][col] = erosion(comp, row, col)
    print('E:', E)

    # Ridge detection
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            O1[row][col] = erosion(comp, row, col)
            O2[row][col] = erosion(comp, row, col)

    makeequalmatrix(helper1, O1, size)
    makeequalmatrix(helper2, O2, size)

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            O1[row][col] = dilation(helper1, row, col)
            O2[row][col] = erosion(helper2, row, col)

    makeequalmatrix(helper3, O2, size)

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            O2[row][col] = dilation(helper3, row, col)

    makeequalmatrix(helper4, O2, size)

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            O2[row][col] = dilation(helper4, row, col)

    # print('O1:', O1)
    # print('O2:', O2)

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if (int(comp[row][col]) - int(O1[row][col]) > 0) and int(comp[row][col]) - int(O2[row][col]) > h:
                R[row][col] = comp[row][col]
            else:
                R[row][col] = 0
    print('R:', R)

    # Comp*
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            compstar[row][col] = max(int(E[row][col]), int(R[row][col]))

    # print('Comp*:', compstar)

    # C8 matrix
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            c8[row][col] = countf(comp, row, col)

    # print('c8 :', c8)

    # Connectivity restoration
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if R[row][col] == 0 and c8[row][col] >= 2:
                compstar[row][col] = comp[row][col]

    # print('Comp*:', compstar)

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