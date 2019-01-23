from Common.functions import imreadgray
from Common.functions import flip
from Common.functions import nearestneighbour
from Common.functions import connectedcomponents
from Common.functions import printmatrix
from Common.functions import find5

img = imreadgray('../Common/fasz2.png')
img2 = imreadgray('../Common/fasz.png')
psi = imreadgray('../Common/fasz2.png')
matrix = imreadgray('../Common/fasz2.png')
matrix2 = imreadgray('../Common/fasz2.png')

flip(img)
flip(img2)
size = img.shape
for row in range(0, size[0]):
    for col in range(0, size[1]):
        psi[row][col] = 0
        matrix[row][col] = 0
        matrix2[row][col] = 0

psi[2][1] = 5
psi[3][2] = 5
psi[3][3] = 5
psi[4][2] = 5
psi[4][3] = 5
psi[4][4] = 5

matrix = nearestneighbour(matrix, psi, 3, 3, 1)
matrix2 = connectedcomponents(matrix2, img, size)

print('Img:')
printmatrix(img)
print('Img2:')
printmatrix(img2)
print('Matrix:')
printmatrix(matrix)
print('Matrix2:')
printmatrix(matrix2)

find5(matrix, matrix2, img, img2, 3, 3)
print('Img after find5:')
printmatrix(img)
