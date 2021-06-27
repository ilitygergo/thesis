import numpy as np
import bcolors
from src.common.functions import *
from common.Algorithm import Algorithm


class KimAlgorithm(Algorithm):
    h = 50

    def __init__(self, img_name):
        self.imgName = img_name
        self.img = get_image_by_name(img_name)
        self.img2 = get_image_by_name(img_name)
        self.comp = get_image_by_name(img_name)
        self.compstar = get_image_by_name(img_name)
        self.c8 = get_image_by_name(img_name)
        self.E = get_image_by_name(img_name)
        self.R = get_image_by_name(img_name)
        self.O1 = get_image_by_name(img_name)
        self.O2 = get_image_by_name(img_name)
        self.helper1 = get_image_by_name(img_name)
        self.helper2 = get_image_by_name(img_name)
        self.kernel = np.ones((3, 3), np.uint8)
        self.kernel2 = np.ones((5, 5), np.uint8)

    def initialize(self):
        for rowIndex in range(0, kim.comp.shape[0]):
            for colIndex in range(0, kim.comp.shape[1]):
                kim.compstar[rowIndex][colIndex] = 0
                kim.c8[rowIndex][colIndex] = 0
                kim.E[rowIndex][colIndex] = 0
                kim.R[rowIndex][colIndex] = 0
                kim.O1[rowIndex][colIndex] = 0
                kim.O2[rowIndex][colIndex] = 0
                kim.helper1[rowIndex][colIndex] = 0
                kim.helper2[rowIndex][colIndex] = 0

        self.kernel[0][0] = 0
        self.kernel[0][2] = 0
        self.kernel[2][0] = 0
        self.kernel[2][2] = 0

        self.kernel2[0][0] = 0
        self.kernel2[0][1] = 0
        self.kernel2[0][3] = 0
        self.kernel2[0][4] = 0
        self.kernel2[1][0] = 0
        self.kernel2[1][4] = 0
        self.kernel2[3][0] = 0
        self.kernel2[3][4] = 0
        self.kernel2[4][0] = 0
        self.kernel2[4][1] = 0
        self.kernel2[4][3] = 0
        self.kernel2[4][4] = 0

    def step(self):
        self.E = cv2.erode(self.comp, self.kernel, iterations=1)
        self.helper1 = cv2.erode(self.comp, self.kernel, iterations=1)
        self.helper2 = cv2.erode(self.comp, self.kernel2, iterations=1)
        self.O1 = cv2.dilate(self.helper1, self.kernel, iterations=1)
        self.O2 = cv2.dilate(self.helper2, self.kernel2, iterations=1)

        for rowIndex in range(1, self.comp.shape[0] - 1):
            for colIndex in range(1, self.comp.shape[1] - 1):
                if (int(self.comp[rowIndex][colIndex]) - int(self.O1[rowIndex][colIndex]) > 0) and int(self.comp[rowIndex][colIndex]) - int(
                        self.O2[rowIndex][colIndex]) > KimAlgorithm.h:
                    self.R[rowIndex][colIndex] = self.comp[rowIndex][colIndex]
                else:
                    self.R[rowIndex][colIndex] = 0

        for rowIndex in range(1, self.comp.shape[0] - 1):
            for colIndex in range(1, self.comp.shape[1] - 1):
                self.compstar[rowIndex][colIndex] = max(int(self.E[rowIndex][colIndex]), int(self.R[rowIndex][colIndex]))

        for rowIndex in range(1, self.comp.shape[0] - 1):
            for colIndex in range(1, self.comp.shape[1] - 1):
                self.c8[rowIndex][colIndex] = countf(self.comp, rowIndex, colIndex)

        for rowIndex in range(1, self.comp.shape[0] - 1):
            for colIndex in range(1, self.comp.shape[1] - 1):
                if self.c8[rowIndex][colIndex] >= 2:
                    self.compstar[rowIndex][colIndex] = self.comp[rowIndex][colIndex]

        makeequalmatrix(self.comp, self.compstar, self.comp.shape)

    def clear_helpers(self):
        pass

    def after_processing(self):
        for rowIndex in range(0, self.comp.shape[0]):
            for colIndex in range(0, self.comp.shape[1]):
                self.R[rowIndex][colIndex] = 0
                self.O1[rowIndex][colIndex] = 0
                self.O2[rowIndex][colIndex] = 0
                self.helper1[rowIndex][colIndex] = 0
                self.helper2[rowIndex][colIndex] = 0

        helper1 = cv2.erode(self.comp, self.kernel, iterations=1)
        helper2 = cv2.erode(self.comp, self.kernel2, iterations=1)
        self.O1 = cv2.dilate(helper1, self.kernel, iterations=1)
        self.O2 = cv2.dilate(helper2, self.kernel2, iterations=1)

        for rowIndex in range(1, self.comp.shape[0] - 1):
            for colIndex in range(1, self.comp.shape[1] - 1):
                if (int(self.comp[rowIndex][colIndex]) - int(self.O1[rowIndex][colIndex]) > 0) and int(self.comp[rowIndex][colIndex]) - int(
                        self.O2[rowIndex][colIndex]) > KimAlgorithm.h:
                    self.R[rowIndex][colIndex] = self.comp[rowIndex][colIndex]
                else:
                    self.R[rowIndex][colIndex] = 0

    def print_algorithm_name(self):
        print(bcolors.OK, r"""
          _  ___             _                  _____ _           _ 
         | |/ (_)           | |                / ____| |         (_)
         | ' / _ _ __ ___   | |     ___  ___  | |    | |__   ___  _ 
         |  < | | '_ ` _ \  | |    / _ \/ _ \ | |    | '_ \ / _ \| |
         | . \| | | | | | | | |___|  __/  __/ | |____| | | | (_) | |
         |_|\_\_|_| |_| |_| |______\___|\___|  \_____|_| |_|\___/|_|
        """, bcolors.ENDC)


kim = KimAlgorithm('shapes.png')
kim.initialize()

while True:
    kim.step()

    if equalmatrix(kim.comp, kim.img2, kim.comp.shape):
        break
    else:
        makeequalmatrix(kim.img2, kim.comp, kim.comp.shape)

kim.after_processing()
save_image_by_name(kim.imgName, kim.R)
