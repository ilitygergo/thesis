import cv2
import json
import bcolors
from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import equalmatrix
from Common.functions import makeequalmatrix
from Common.functions import borderpoint8
from Common.functions import eightcomponent

print(bcolors.OK, "   _____                       _             _           _ ")
print("  / ____|                     (_)           | |         | |")
print(" | |     ___  _   _ _ __  _ __ _  ___    ___| |_    __ _| |")
print(" | |    / _ \| | | | '_ \| '__| |/ _ \  / _ \ __|  / _` | |")
print(" | |___| (_) | |_| | |_) | |  | |  __/ |  __/ |_  | (_| | |")
print("  \_____\___/ \__,_| .__/|_|  |_|\___|  \___|\__|  \__,_|_|")
print("                   | |                                     ")
print("                   |_|                                     ", bcolors.ENDC)

# Reading in the pictures as a gray picture
picture = 'sima'

img = imreadgray('../Common/' + picture + '.png')
img2 = imreadgray('../Common/' + picture + '.png')
helper = imreadgray('../Common/' + picture + '.png')

# Converting values 0-255
img = flip(img)
img2 = flip(img2)
helper = flip(helper)

# Initialization
lepes = 0
size = img.shape

# Lookup table
exDict = {1:1, 2:2, 3:3}
exDict = {'exDict': exDict}
with open('lookup.txt', 'w') as file:
    file.write(json.dumps(exDict))

print(img)

while True:

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if not borderpoint8(img, row, col):
                continue
            if not eightcomponent(img, row, col):
                continue
            helper[row][col] = 1

    print(helper)

    lepes += 1
    if equalmatrix(img, img2, size):
        break
    else:
        makeequalmatrix(img2, img, size)

# Converting the values back to normal
flip(img)

# Saving
cv2.imwrite('results/' + picture + '.png', img)
