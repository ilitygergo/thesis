import bcolors
from modules.functions import imreadgray
from modules.functions import flip
from modules.functions import minimizenotnull
from modules.functions import maximizenotnull

print(bcolors.OK, "                       _ _ _   _____                      _ _       ")
print("     /\                | | (_) |  __ \                    | | |      ")
print("    /  \   _ __ ___ ___| | |_  | |__) |__ _ _ __ ___   ___| | | __ _ ")
print("   / /\ \ | '__/ __/ _ \ | | | |  _  // _` | '_ ` _ \ / _ \ | |/ _` |")
print("  / ____ \| | | (_|  __/ | | | | | \ \ (_| | | | | | |  __/ | | (_| |")
print(" /_/    \_\_|  \___\___|_|_|_| |_|  \_\__,_|_| |_| |_|\___|_|_|\__,_|", bcolors.ENDC)

# Beolvasás szürkeárnyalatos képként
picture = 'sima'

img = imreadgray('../pictures/' + picture + '.png')
img2 = imreadgray('../pictures/' + picture + '.png')
helper = imreadgray('../pictures/' + picture + '.png')

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

#for row in range(1, size[0] - 1):
#    for col in range(1, size[1] - 1):
#        if helper[row][col] == 0:
#            if img2[row][col] != 0:

