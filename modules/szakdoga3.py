import bcolors
import matplotlib.pyplot as plt
from modules.functions import imreadgray
from modules.functions import flip
from modules.functions import localmaximum
from modules.functions import endpoint


# If one of the neighbours of point has a value 0 than it is true
def borderpoint(n1, n3, n5, n7):
    if n1 == 0 or n3 == 0 or n5 == 0 or n7 == 0:
        return False
    return True


print(bcolors.OK, "  _____       _            _        _____ _       ")
print("  / ____|     | |          (_)      / ____(_)      ")
print(" | (___   __ _| | __ _ _ __ _ _____| (___  _ _   _ ")
print("  \___ \ / _` | |/ _` | '__| |______\___ \| | | | |")
print("  ____) | (_| | | (_| | |  | |      ____) | | |_| |")
print(" |_____/ \__,_|_|\__,_|_|  |_|     |_____/|_|\__, |")
print("                                              __/ |")
print("                                             |___/ ", bcolors.ENDC)

# Reading in the pictures as a gray picture
picture = 'sima'

img = imreadgray('../pictures/' + picture + '.png')
img2 = imreadgray('../pictures/' + picture + '.png')
ave = imreadgray('../pictures/' + picture + '.png')
g1 = imreadgray('../pictures/' + picture + '.png')
g2 = imreadgray('../pictures/' + picture + '.png')

# Converting the values 0-255
img = flip(img)
img2 = flip(img2)
ave = flip(ave)
g1 = flip(g1)
g2 = flip(g2)

# Initialization
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

# Smoothing by the 5 condition
for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        if img[row][col] != 0:
            if borderpoint(img[row][col + 1], img[row - 1][col], img[row][col - 1], img[row + 1][col]):
                continue
            if localmaximum(img[row][col], img[row][col + 1], img[row - 1][col + 1],
                             img[row - 1][col], img[row - 1][col - 1], img[row][col - 1],
                             img[row + 1][col - 1], img[row + 1][col], img[row + 1][col + 1]):
                continue
            if endpoint(img, row, col):
                continue
            img[row][col] = 0

print(img)
