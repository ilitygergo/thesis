import bcolors
import matplotlib.pyplot as plt
from modules.functions import imreadgray
from modules.functions import flip

print(bcolors.OK, "  _____       _            _        _____ _       ")
print("  / ____|     | |          (_)      / ____(_)      ")
print(" | (___   __ _| | __ _ _ __ _ _____| (___  _ _   _ ")
print("  \___ \ / _` | |/ _` | '__| |______\___ \| | | | |")
print("  ____) | (_| | | (_| | |  | |      ____) | | |_| |")
print(" |_____/ \__,_|_|\__,_|_|  |_|     |_____/|_|\__, |")
print("                                              __/ |")
print("                                             |___/ ", bcolors.ENDC)

# Beolvasás szürkeárnyalatos képként
picture = 'sima'

img = imreadgray('../pictures/' + picture + '.png')
img2 = imreadgray('../pictures/' + picture + '.png')
ave = imreadgray('../pictures/' + picture + '.png')
g1 = imreadgray('../pictures/' + picture + '.png')
g2 = imreadgray('../pictures/' + picture + '.png')

# Értékek átkonvertálása 0-255
img = flip(img)
img2 = flip(img2)
ave = flip(ave)
g1 = flip(g1)
g2 = flip(g2)

# Inicializálás
y, x, _ = plt.hist(img)
maximum = max(x)
size = img.shape

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        a = int(img[row][col - 1])
        b = int(img[row][col + 1])
        c = int(img[row - 1][col])
        d = int(img[row + 1][col])
        ave[row][col] = (a + b + c + d) / 4

print(img)

# Central grey distance transform

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        a = int(img[row - 1][col - 1])
        b = int(img[row - 1][col])
        c = int(img[row - 1][col + 1])
        d = int(img[row][col - 1])
        g1[row][col] = (a + b + c + d) * (int(ave[row][col]) / maximum)**2 + int(img[row][col])

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        a = int(img[row + 1][col + 1])
        b = int(img[row + 1][col])
        c = int(img[row + 1][col - 1])
        d = int(img[row][col + 1])
        g2[row][col] = (a + b + c + d) * (int(ave[row][col]) / maximum)**2 + int(img[row][col])

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        img[row][col] = min(g1[row][col], g2[row][col])

print(img)
