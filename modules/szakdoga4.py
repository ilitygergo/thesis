import bcolors
from modules.functions import imreadgray
from modules.functions import flip

print(bcolors.OK, " _  __                    _____       _       _  ___           ")
print(" | |/ /                   / ____|     | |     | |/ (_)          ")
print(" | ' / __ _ _ __   __ _  | (___  _   _| |__   | ' / _ _ __ ___  ")
print(" |  < / _` | '_ \ / _` |  \___ \| | | | '_ \  |  < | | '_ ` _ \ ")
print(" | . \ (_| | | | | (_| |  ____) | |_| | | | | | . \| | | | | | |")
print(" |_|\_\__,_|_| |_|\__, | |_____/ \__,_|_| |_| |_|\_\_|_| |_| |_|")
print("                   __/ |                                        ")
print("                  |___/                                         ", bcolors.ENDC)

# Beolvasás szürkeárnyalatos képként
picture = 'sima'

img = imreadgray('../pictures/' + picture + '.png')
psi = imreadgray('../pictures/' + picture + '.png')
skeleton = imreadgray('../pictures/' + picture + '.png')

# Értékek átkonvertálása 0-255
flip(img)
flip(psi)
flip(skeleton)

# Initialization
size = img.shape
psivalue = 6

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        psi[row][col] = 0

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

print(img)
print(psi)
