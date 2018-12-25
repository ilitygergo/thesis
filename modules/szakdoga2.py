import bcolors
from modules.function import imreadgray
from modules.function import flip
from modules.function import minimizenotnull
from modules.function import maximizenotnull

print(bcolors.HEADER, 'Carlo Arcelli and Giuliana Ramella algoritmus:', bcolors.ENDC)

# Beolvasás szürkeárnyalatos képként
img = imreadgray('../pictures/hollow.jpg')
img2 = imreadgray('../pictures/hollow.jpg')
helper = imreadgray('../pictures/hollow.jpg')

# Értékek átkonvertálása 0-255
img = flip(img)
img2 = flip(img2)
helper = flip(helper)

# Inicializálás
size = img.shape
h = 0
n = size[0]
m = size[1]
matrix = [0] * n
for x in range(n):
    matrix[x] = [0] * m
print(img2, '\n')

# 1 Simítás minimalizálás és maximalizálás

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if img2[row][col] != 0:
            img2[row][col] = minimizenotnull(img[row][col], img[row-1][col], img[row+1][col], img[row][col-1], img[row][col+1])

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if img2[row][col] != 0:
            img2[row][col] = maximizenotnull(img[row][col], img[row-1][col], img[row-1][col-1], img[row][col-1], img[row+1][col-1] , img[row+1][col], img[row+1][col+1], img[row][col+1], img[row+1][col+1])

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        img[row][col] = img2[row][col]
        helper[row][col] = img2[row][col]

# 2 Üregfeltöltés

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if img2[row][col] != 0:
            if img2[row][col] <= img2[row+1][col] and img2[row][col] <= img2[row-1][col] and img2[row][col] <= img2[row][col+1] and img2[row][col] <= img2[row][col-1]:
                helper[row][col] = 0

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if helper[row][col] == 0:
            if img2[row][col] != 0:
                if img2[row][col] == img2[row+1][col] or img2[row][col] == img2[row-1][col] or img2[row][col] == img2[row][col+1] or img2[row][col] == img2[row][col-1]:
                    helper[row][col] = 0

print(helper, '\n')

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if helper[row][col] == 0:
            if img2[row][col] != 0:

