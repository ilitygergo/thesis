import cv2
import numpy as np
import bcolors
from src.Common.functions import imreadgray
from src.Common.functions import flip
from src.Common.functions import equalmatrix
from src.Common.functions import makeequalmatrix
from src.Common.functions import countf

print(bcolors.OK, " _  ___             _                  _____ _           _ ")
print(" | |/ (_)           | |                / ____| |         (_)")
print(" | ' / _ _ __ ___   | |     ___  ___  | |    | |__   ___  _ ")
print(" |  < | | '_ ` _ \  | |    / _ \/ _ \ | |    | '_ \ / _ \| |")
print(" | . \| | | | | | | | |___|  __/  __/ | |____| | | | (_) | |")
print(" |_|\_\_|_| |_| |_| |______\___|\___|  \_____|_| |_|\___/|_|", bcolors.ENDC)

# Reading in the image as a gray image
picture = 'fingerprintmini'

img = imreadgray('../Common/' + picture + '.png')
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
h = 50
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

equal = True
lepes = 1
kernel = np.ones((3, 3), np.uint8)
kernel2 = np.ones((5, 5), np.uint8)

kernel[0][0] = 0
kernel[0][2] = 0
kernel[2][0] = 0
kernel[2][2] = 0

kernel2[0][0] = 0
kernel2[0][1] = 0
kernel2[0][3] = 0
kernel2[0][4] = 0
kernel2[1][0] = 0
kernel2[1][4] = 0
kernel2[3][0] = 0
kernel2[3][4] = 0
kernel2[4][0] = 0
kernel2[4][1] = 0
kernel2[4][3] = 0
kernel2[4][4] = 0

print(kernel)
print(kernel2)

print('Comp:')
print(comp)

while equal:

    # Erosion
    E = cv2.erode(comp, kernel, iterations=1)
    # print('E:', E)

    # Ridge detection
    helper1 = cv2.erode(comp, kernel, iterations=1)
    helper2 = cv2.erode(comp, kernel2, iterations=1)

    O1 = cv2.dilate(helper1, kernel, iterations=1)
    O2 = cv2.dilate(helper2, kernel2, iterations=1)

    # print('O1:', O1)
    # print('O2:', O2)

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if (int(comp[row][col]) - int(O1[row][col]) > 0) and int(comp[row][col]) - int(O2[row][col]) > h:
                R[row][col] = comp[row][col]
            else:
                R[row][col] = 0
    # print('R:', R)

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
            if c8[row][col] >= 2:
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

# Ridge detection once more
for row in range(0, size[0]):
    for col in range(0, size[1]):
        R[row][col] = 0
        O1[row][col] = 0
        O2[row][col] = 0
        helper1[row][col] = 0
        helper2[row][col] = 0

# Ridge detection
helper1 = cv2.erode(comp, kernel, iterations=1)
helper2 = cv2.erode(comp, kernel2, iterations=1)

O1 = cv2.dilate(helper1, kernel, iterations=1)
O2 = cv2.dilate(helper2, kernel2, iterations=1)

# print('O1:', O1)
# print('O2:', O2)

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if (int(comp[row][col]) - int(O1[row][col]) > 0) and int(comp[row][col]) - int(O2[row][col]) > h:
            R[row][col] = comp[row][col]
        else:
            R[row][col] = 0
# print('R:', R)

print(comp, '\n', bcolors.ENDC)

# Converting the values back to normal
flip(R)

# Saving
cv2.imwrite('results/' + picture + '.png', R)