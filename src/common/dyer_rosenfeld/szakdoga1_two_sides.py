import cv2
import bcolors
import numpy as np
from src.common.functions import rvalue
from src.common.functions import minimize
from src.common.functions import imreadgray
from src.common.functions import notendpoint
from src.common.functions import flip
from src.common.functions import connected
from src.common.functions import equalmatrix
from src.common.functions import makeequalmatrix

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

img = imreadgray('../files/input/' + picture + '.png')
img2 = imreadgray('../files/input/' + picture + '.png')

# Értékek átkonvertálása 0-255
img = flip(img)

# Lépésszámláló és inicializálás
lepes = 1
size = img.shape
nemegyenlo = True
for row in range(0, size[0]):
    for col in range(0, size[1]):
        img2[row][col] = 0

while nemegyenlo:

    # Folyton ismétlődő inicializálás
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

    # Mátrixok
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

    # Határpontok megkeresése

    for oldal in range(0, 4):
        if oldal == 0:
            print(bcolors.OK, 'Északi határpontok:', bcolors.ENDC)
        elif oldal == 1:
            print(bcolors.OK, 'Nyugati határpontok:', bcolors.ENDC)
        elif oldal == 2:
            print(bcolors.OK, 'Déli határpontok:', bcolors.ENDC)
        elif oldal == 3:
            print(bcolors.OK, 'Keleti határpontok:', bcolors.ENDC)
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
                if oldal == 0 or oldal == 1:
                    if b < e - grayness:
                        hatar += 1
                        matrix[row - 1][col - 1] = e
                        matrix2[row][col] = 'X'
                    else:
                        matrix2[row][col] = ' '
                if oldal == 0 or oldal == 1:
                    if d < e - grayness:
                        hatar += 1
                        matrix[row - 1][col - 1] = e
                        matrix2[row][col] = 'X'
                    else:
                        matrix2[row][col] = ' '
                if oldal == 2 or oldal == 3:
                    if h < e - grayness:
                        hatar += 1
                        matrix[row - 1][col - 1] = e
                        matrix2[row][col] = 'X'
                    else:
                        matrix2[row][col] = ' '
                if oldal == 2 or oldal == 3:
                    if f < e - grayness:
                        hatar += 1
                        matrix[row - 1][col - 1] = e
                        matrix2[row][col] = 'X'
                    else:
                        matrix2[row][col] = ' '

        print(np.matrix(matrix2))
        print('\n')
        print('Összesen:', hatar)

        # Minimalizálás végpont és összefüggőség alapján
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
                    if notendpoint(b, d, h, f, e - grayness) and connected(a, b, c, d, e, f, g, h, i, grayness) and img[row][col] != 0:
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

        print('Törölhető:', bcolors.ERR, igen, bcolors.ENDC)
        print('Nem törölhető:', bcolors.OK, nem, bcolors.ENDC, '\n')
        print(bcolors.OK, 'Output:', bcolors.ENDC)
        print(bcolors.BOLD, img, bcolors.ENDC)
    print(bcolors.BLUE, '\n', lepes, '. lépés eredménye:')
    print(img, '\n', bcolors.ENDC)

    # Making sure that the function runs until the image has no points left to remove
    lepes += 1
    if equalmatrix(img, img2, size):
        break
    else:
        makeequalmatrix(img2, img, size)

# Értékek visszakonvertálása
img = flip(img)

# Kiíratás vagy mentés
cv2.imwrite('results/two_sides/' + picture + '.png', img)
