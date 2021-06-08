import bcolors
from common.functions import *
from szakdoga1 import DyerRosenfeldAlgorithm


class DyerRosenfeldAlgorithmTwoSides(DyerRosenfeldAlgorithm):
    def find_border_points(self, side):
        for rowIndex in range(1, self.img.shape[0] - 1):
            for colIndex in range(1, (self.img.shape[1] - 1)):
                b = self.img[rowIndex - 1, colIndex]
                d = self.img[rowIndex, colIndex - 1]
                e = self.img[rowIndex, colIndex]
                f = self.img[rowIndex, colIndex + 1]
                h = self.img[rowIndex + 1, colIndex]
                grayness = rvalue(b, d, e, f, h) * self.percent
                if side == self.NORTH_BORDER and side == self.WEST_BORDER and b < e - grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])
                if side == self.SOUTH_BORDER and side == self.EAST_BORDER and h < e - grayness:
                    self.borderPointPixels.append([rowIndex, colIndex, e])


dyerTwoSides = DyerRosenfeldAlgorithmTwoSides(get_image_by_name('shapes.png'))
DyerRosenfeldAlgorithmTwoSides.print_algorithm_name()

while True:
    print(bcolors.BOLD, dyerTwoSides.img, bcolors.ENDC, '\n')
    dyerTwoSides.step()
    dyerTwoSides.clear_helpers()

    if equalmatrix(dyerTwoSides.img, dyerTwoSides.imgBeforeStep, dyerTwoSides.img.shape):
        break
    else:
        makeequalmatrix(dyerTwoSides.imgBeforeStep, dyerTwoSides.img, dyerTwoSides.img.shape)

flip(dyerTwoSides.img)
cv2.imwrite('test.png', dyerTwoSides.img)
