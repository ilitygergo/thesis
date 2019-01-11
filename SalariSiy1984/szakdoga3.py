import cv2
import bcolors
import matplotlib.pyplot as plt
from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import localmaximum
from Common.functions import endpoint
from Common.functions import connectedcorner
from Common.functions import connectedpath
from Common.functions import equalmatrix
from Common.functions import makeequalmatrix
from Common.functions import borderpoint

print(bcolors.OK, "  _____       _            _        _____ _       ")
print("  / ____|     | |          (_)      / ____(_)      ")
print(" | (___   __ _| | __ _ _ __ _ _____| (___  _ _   _ ")
print("  \___ \ / _` | |/ _` | '__| |______\___ \| | | | |")
print("  ____) | (_| | | (_| | |  | |      ____) | | |_| |")
print(" |_____/ \__,_|_|\__,_|_|  |_|     |_____/|_|\__, |")
print("                                              __/ |")
print("                                             |___/ ", bcolors.ENDC)

# Reading in the pictures as a gray picture
picture = 'test'

img = imreadgray('../Common/' + picture + '.png')
img2 = imreadgray('../Common/' + picture + '.png')
helper = imreadgray('../Common/' + picture + '.png')
g1 = imreadgray('../Common/' + picture + '.png')
g2 = imreadgray('../Common/' + picture + '.png')

# Converting the values 0-255
flip(img)

# Initialization
size = img.shape
notequal = True
lepes = 1

for row in range(size[0]):
    for col in range(size[1]):
        if row == 0 or col == 0 or row == size[0] or col == size[1]:
            img[row][col] = 0
        img2[row][col] = 0
        helper[row][col] = 0
        g1[row][col] = 0
        g2[row][col] = 0

print(img)
maximum = 1

# Central grey distance transform
for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        a = int(img[row - 1][col - 1])
        b = int(img[row - 1][col])
        c = int(img[row - 1][col + 1])
        d = int(img[row][col - 1])
        ave = (int(img[row][col - 1]) + int(img[row][col + 1]) + int(img[row - 1][col]) + int(
            img[row + 1][col])) / 4
        plus = (ave / maximum)**2
        g1[row][col] = int(img[row][col]) + min(a, b, c, d) * plus

for row in reversed(range(1, size[0] - 1)):
    for col in reversed(range(1, size[1] - 1)):
        a = int(img[row + 1][col + 1])
        b = int(img[row + 1][col])
        c = int(img[row + 1][col - 1])
        d = int(img[row][col + 1])
        ave = (int(img[row][col - 1]) + int(img[row][col + 1]) + int(img[row - 1][col]) + int(
            img[row + 1][col])) / 4
        plus = (ave / maximum)**2
        g2[row][col] = int(img[row][col]) + min(a, b, c, d) * plus

for row in range(size[0]):
    for col in range(size[1]):
        img[row][col] = min(int(g1[row][col]), int(g2[row][col]))
        helper[row][col] = min(int(g1[row][col]), int(g2[row][col]))

print(bcolors.BLUE, 'CGDT:', img, bcolors.ENDC)

# Smoothing by the 5 condition
while notequal:
    hatar = 0
    localmax = 0
    end = 0
    conc = 0
    conp = 0
    torolt = 0
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if img[row][col] != 0:
                if borderpoint(img[row][col + 1], img[row - 1][col], img[row][col - 1], img[row + 1][col]):
                    hatar += 1
                    if localmaximum(img[row][col], img[row][col + 1], img[row - 1][col + 1],
                                     img[row - 1][col], img[row - 1][col - 1], img[row][col - 1],
                                     img[row + 1][col - 1], img[row + 1][col], img[row + 1][col + 1]):
                        localmax += 1
                        continue
                    if endpoint(img, row, col):
                        end += 1
                        continue
                    if not connectedcorner(img, row, col):
                        conc += 1
                        continue
                    if not connectedpath(img, row, col):
                        conp += 1
                        continue
                    torolt += 1
                    helper[row][col] = 0

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            img[row][col] = helper[row][col]

    print(bcolors.WARN, '\n', lepes, '. run:', bcolors.ENDC)
    print(img, '\n')

    print('Borders: ', hatar)
    print('LocalMax:', localmax)
    print('Endpoints:', end)
    print('ConnectedCorner:', conc)
    print('ConnectedPath:', conp)
    print('Deleted:', bcolors.ERR, torolt, bcolors.ENDC)

    # Making sure that the function runs until the image has no points left to remove
    lepes += 1

    if equalmatrix(img, img2, size):
        break
    else:
        makeequalmatrix(img2, img, size)

# Saving
flip(img)
cv2.imwrite('results/' + picture + '.png', img)
