import cv2
import bcolors
import matplotlib.pyplot as plt
from modules.functions import imreadgray
from modules.functions import flip
from modules.functions import localmaximum
from modules.functions import endpoint
from modules.functions import connectedcorner
from modules.functions import connectedpath
from modules.functions import equalmatrix
from modules.functions import makeequalmatrix
from modules.functions import borderpoint
from modules.functions import gif

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
helper = imreadgray('../pictures/' + picture + '.png')
ave = imreadgray('../pictures/' + picture + '.png')
g1 = imreadgray('../pictures/' + picture + '.png')
g2 = imreadgray('../pictures/' + picture + '.png')

# Converting the values 0-255
flip(img)
flip(img2)
flip(helper)
flip(ave)
flip(g1)
flip(g2)

# Initialization
y, x, _ = plt.hist(img)
maximum = int(max(x))
size = img.shape
notequal = True
lepes = 1

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

for row in range(size[0] - 1, 1):
    for col in range(size[1] - 1, 1):
        a = int(img[row + 1][col + 1])
        b = int(img[row + 1][col])
        c = int(img[row + 1][col - 1])
        d = int(img[row][col + 1])
        g2[row][col] = (a + b + c + d) * (int(ave[row][col]) / maximum)**2 + int(img[row][col])

for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        img[row][col] = min(g1[row][col], g2[row][col])
        helper[row][col] = min(g1[row][col], g2[row][col])

print(bcolors.BLUE, 'CGDT:', img, bcolors.ENDC)
# gif(img, 0)

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
    print('Deleted:', torolt)
    # gif(img, lepes)

    # Making sure that the function runs until the image has no points left to remove
    lepes += 1

    if equalmatrix(img, img2, size):
        break
    else:
        makeequalmatrix(img2, img, size)

# Saving
flip(img)
cv2.imwrite('../results/szakdoga3/' + picture + '.png', img)
