import bcolors
from common.Algorithm import Algorithm
from src.common.functions import *


class SalarySiyAlgorithm(Algorithm):

    def __init__(self, img_name):
        self.img = get_image_by_name(img_name)
        self.img2 = get_image_by_name(img_name)
        self.g1 = get_image_by_name(img_name)
        self.g2 = get_image_by_name(img_name)
        self.borders = get_image_by_name(img_name)

    def step(self):
        pass

    def clear_helpers(self):
        pass

    def print_algorithm_name(self):
        print(bcolors.OK, r"""
                  _____       _            _        _____ _       
                 / ____|     | |          (_)      / ____(_)      
                | (___   __ _| | __ _ _ __ _ _____| (___  _ _   _ 
                 \___ \ / _` | |/ _` | '__| |______\___ \| | | | |
                 ____) | (_| | | (_| | |  | |      ____) | | |_| |
                |_____/ \__,_|_|\__,_|_|  |_|     |_____/|_|\__, |
                                                             __/ |
                                                            |___/
                """, bcolors.ENDC)


salary_siy = SalarySiyAlgorithm('shapes.png')

# Initialization
size = salary_siy.img.shape
notequal = True
hist = [0] * 256
maximum = 0
maxima = 0

for row in range(size[0]):
    for col in range(size[1]):
        if row == 0 or col == 0 or row == size[0] or col == size[1]:
            salary_siy.img[row][col] = 0
        salary_siy.g1[row][col] = 0
        salary_siy.g2[row][col] = 0
        salary_siy.borders[row][col] = 0

for row in range(size[0]):
    for col in range(size[1]):
        hist[int(salary_siy.img[row][col])] += 1

for a in range(256):
    if a == 0:
        continue
    if maxima < hist[a]:
        maxima = hist[a]
        maximum = a

# Central grey distance transform
for row in range(1, size[0] - 1):
    for col in range(1, size[1] - 1):
        a = salary_siy.g1[row - 1][col - 1]
        b = salary_siy.g1[row - 1][col]
        c = salary_siy.g1[row - 1][col + 1]
        d = salary_siy.g1[row][col - 1]
        ave = (int(salary_siy.img[row][col - 1]) + int(salary_siy.img[row][col + 1]) + int(salary_siy.img[row - 1][col]) + int(salary_siy.img[row + 1][col])) / 4
        plus = (int(ave) / maximum)**2
        if int(salary_siy.img[row][col]) + int(min(a, b, c, d) * plus) > 255:
            salary_siy.g1[row][col] = 255
        else:
            salary_siy.g1[row][col] = int(salary_siy.img[row][col]) + int(min(a, b, c, d) * int(plus))

for row in reversed(range(1, size[0] - 1)):
    for col in reversed(range(1, size[1] - 1)):
        a = salary_siy.g2[row + 1][col + 1]
        b = salary_siy.g2[row + 1][col]
        c = salary_siy.g2[row + 1][col - 1]
        d = salary_siy.g2[row][col + 1]
        ave = (int(salary_siy.img[row][col - 1]) + int(salary_siy.img[row][col + 1]) + int(salary_siy.img[row - 1][col]) + int(salary_siy.img[row + 1][col])) / 4
        plus = (ave / maximum)**2
        if (int(salary_siy.img[row][col]) + int(min(a, b, c, d) * plus)) > 255:
            salary_siy.g2[row][col] = 255
        else:
            salary_siy.g2[row][col] = int(salary_siy.img[row][col]) + int(min(a, b, c, d) * plus)

for row in range(size[0]):
    for col in range(size[1]):
        salary_siy.img[row][col] = min(salary_siy.g1[row][col], salary_siy.g2[row][col])

print(bcolors.BLUE, 'CGDT:', salary_siy.img, bcolors.ENDC)

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
            if borderpoint(salary_siy.img, row, col):
                hatar += 1
                salary_siy.borders[row][col] = 1

    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if salary_siy.img[row][col] != 0:
                if salary_siy.borders[row][col] == 1:
                    if localmaximum(salary_siy.img[row][col], salary_siy.img[row][col + 1], salary_siy.img[row - 1][col + 1],
                                     salary_siy.img[row - 1][col], salary_siy.img[row - 1][col - 1], salary_siy.img[row][col - 1],
                                     salary_siy.img[row + 1][col - 1], salary_siy.img[row + 1][col], salary_siy.img[row + 1][col + 1]):
                        localmax += 1
                        continue
                    if endpoint(salary_siy.img, row, col):
                        end += 1
                        continue
                    if not connectedcorner(salary_siy.img, row, col):
                        conc += 1
                        continue
                    if not connectedpath(salary_siy.img, row, col):
                        conp += 1
                        continue
                    torolt += 1
                    salary_siy.img[row][col] = 0

    if equalmatrix(salary_siy.img, salary_siy.img2, size):
        break
    else:
        makeequalmatrix(salary_siy.img2, salary_siy.img, size)

save_image_by_name('text.png', salary_siy.img)
