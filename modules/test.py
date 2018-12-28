from modules.functions import nearestneighbour
from modules.functions import imreadgray
from modules.functions import flip
from modules.functions import printmatrix

img = imreadgray('../pictures/test2.png')
img = flip(img)
size = img.shape
n = size[0]
m = size[1]
matrix = ['O'] * n
for x in range(n):
    matrix[x] = ['O'] * m

matrix[2][3] = 'X'

print(img)
printmatrix(matrix)

nearestneighbour(matrix, img, 2, 3)

printmatrix(matrix)
