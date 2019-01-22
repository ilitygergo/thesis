import cv2
import bcolors
import copy
import numpy as np
import itertools


# Reads a colored picture in gray
def imreadgray(img):
    image = cv2.imread(img)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return img


# Flips the values of a gray image to have 0 as white and 255 as black
def flip(img):
    size = img.shape
    for row in range(0, size[0]):
        for col in range(0, (size[1])):
            img[row, col] = 255 - img[row, col]
    return img


# Calculates the value of R'
def rvalue(b, d, e, f, h):
    minimum = 0
    maximum = 0
    index = 0
    neighbour = [b, d, e, f, h]
    while index < 4:
        if minimum > neighbour[index + 1]:
            minimum = neighbour[index + 1]
        index += 1
    index = 0
    while index < 4:
        if maximum < neighbour[index + 1]:
            maximum = neighbour[index + 1]
        index += 1
    r = maximum - minimum + 1
    return r


# Minimizes the given e point by itself and its neighbours
def minimize(b, d, h, f, e):
    ret = b
    index = 0
    neighbour = [b, d, h, f, e]
    while index < 4:
        if ret > neighbour[index+1]:
            ret = neighbour[index+1]
        index += 1
    return ret


# Minimize the given e point by itself and its neighbours if they are not zero
def minimizenotnull(b, d, h, f, e):
    ret = b
    index = 0
    neighbour = [b, d, h, f, e]
    while index < 4:
        if ret > neighbour[index+1] != 0:
            ret = neighbour[index+1]
        index += 1
    return ret


# Maximize the given e point by itself and its neighbours if they are not zero
def maximizenotnull(a, b, c, d, e, f, g, h, i):
    ret = a
    index = 0
    neighbour = [a, b, c, d, e, f, g, h, i]
    while index < 4:
        if ret < neighbour[index+1] != 0:
            ret = neighbour[index+1]
        index += 1
    return ret


# For the given e point check the neighbours if they have a value bigger than (e-R')
def notendpoint(b, d, h, f, r):
    szam = 0
    if b >= r:
        szam += 1
    if d >= r:
        szam += 1
    if h >= r:
        szam += 1
    if f >= r:
        szam += 1
    if szam >= 2:
        # print('True')
        return True
    else:
        # print('False')
        return False


def connected(a, b, c, d, e, f, g, h, i, r):
    connect = [b, d, f, h]
    szam = 0
    ret = 0
    con = 0
    if b-r >= e:
        szam += 1
    if d-r >= e:
        szam += 1
    if f-r >= e:
        szam += 1
    if h-r >= e:
        szam += 1

    for x in range(0, 3):
        for y in range(x + 1, 4):
            if connect[x] < connect[y]:
                m = connect[x]
                if e > (m - r):
                    con += 1
                    continue
                elif findpath(a, b, c, d, f, g, h, i, m, x, y, r):
                    ret += 1
            else:
                m = connect[y]
                if e > (m - r):
                    con += 1
                    continue
                elif findpath(a, b, c, d, f, g, h, i, m, x, y, r):
                    ret += 1
    # print('szam: ', szam)
    # print('con: ', con)
    # print('ret: ', ret)
    if szam == 1:
        print('True')
        return True
    if szam == 2:
        if ret >= 1:
            # print('True')
            # print(ret)
            return True
    elif szam == 3:
        if ret >= 3:
            # print('True')
            return True
    elif szam == 4:
        if ret >= 8:
            # print('True')
            return True
    else:
        # print('False')
        return False


def findpath(a, b, c, d, f, g, h, i, m, x, y, r):
    if x == 0 and y == 1:
        if (b >= (m - r) and a >= (m - r) and d >= (m - r)) or (b >= (m - r) and c >= (m - r) and f >= (m - r) and i >= (m - r) and h >= (m - r) and g >= (m - r) and d >= (m - r)):
            # b and d
            # print('b and d')
            return True
        else:
            return False
    elif x == 0 and y == 2:
        if (b >= (m - r) and c >= (m - r) and f >= (m - r)) or (b >= (m - r) and a >= (m - r) and d >= (m - r) and g >= (m - r) and h >= (m - r) and i >= (m - r) and f >= (m - r)):
            # b and f
            # print('b and f')
            return True
        else:
            return False
    elif x == 0 and y == 3:
        if (b >= (m - r) and a >= (m - r) and d >= (m - r) and g >= (m - r) and h >= (m - r)) or (b >= (m - r) and c >= (m - r) and f >= (m - r) and i >= (m - r) and h >= (m - r)):
            # b and h
            # print('b and h')
            return True
        else:
            return False
    elif x == 1 and y == 2:
        if (d >= (m - r) and a >= (m - r) and b >= (m - r) and c >= (m - r) and f >= (m - r)) or (d >= (m - r) and g >= (m - r) and h >= (m - r) and i >= (m - r) and f >= (m - r)):
            # d and f
            # print('d and f')
            return True
        else:
            return False
    elif x == 1 and y == 3:
        if (d >= (m - r) and g >= (m - r) and h >= (m - r)) or (d >= (m - r) and a >= (m - r) and b >= (m - r) and c >= (m - r) and f >= (m - r) and i >= (m - r) and h >= (m - r)):
            # d and h
            # print('d and h')
            return True
        else:
            return False
    elif x == 2 and y == 3:
        if (f >= (m - r) and i >= (m - r) and h >= (m - r)) or (f >= (m - r) and c >= (m - r) and b >= (m - r) and a >= (m - r) and d >= (m - r) and g >= (m - r) and h >= (m - r)):
            # f and h
            # print('f and h')
            return True
        else:
            return False
    else:
        return False


# Checks wether a matrix is equal to another one
def equalmatrix(mat1, mat2, size):
    for row in range(1, size[0] - 1):
        for col in range(1, size[1] - 1):
            if mat1[row][col] != mat2[row][col]:
                return False
    return True


# Makes matrix1 equal to matrix2
def makeequalmatrix(mat1, mat2, size):
    for row in range(0, size[0]):
        for col in range(0, size[1]):
            mat1[row][col] = mat2[row][col]


# Prints out the matrix
def printmatrix(matrix):
    if len(matrix) < 15:
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in matrix]))
        print('\n')


# Finds pixels with same value and returns a matrix
def nearestneighbour(matrix, img, r, c):
    stack = []
    x = copy.deepcopy(r)
    y = copy.deepcopy(c)

    while True:
        if img[x][y] == img[x - 1][y] and matrix[x - 1][y] == 'X':
            # print(bcolors.WARN, 'up', bcolors.ENDC)
            stack.append([x, y])
            matrix[x][y] = 'O'
            x -= 1
            # printmatrix(matrix)
        elif img[x][y] == img[x][y + 1] and matrix[x][y + 1] == 'X':
            # print(bcolors.WARN, 'right', bcolors.ENDC)
            stack.append([x, y])
            matrix[x][y] = 'O'
            y += 1
            # printmatrix(matrix)
        elif img[x][y] == img[x + 1][y] and matrix[x + 1][y] == 'X':
            # print(bcolors.WARN, 'down', bcolors.ENDC)
            stack.append([x, y])
            matrix[x][y] = 'O'
            x += 1
            # printmatrix(matrix)
        elif img[x][y] == img[x][y - 1] and matrix[x][y - 1] == 'X':
            # print(bcolors.WARN, 'left', bcolors.ENDC)
            stack.append([x, y])
            matrix[x][y] = 'O'
            y -= 1
            # printmatrix(matrix)
        elif len(stack) > 0:
            # print(bcolors.WARN, 'pop', bcolors.ENDC)
            value = stack.pop()
            matrix[x][y] = 'O'
            x = value[0]
            y = value[1]
        elif len(stack) == 0:
            matrix[x][y] = 'O'
            break

    return matrix


# If one of the neighbours of point has a value 0 than it is true
def borderpoint(n1, n3, n5, n7):
    if n1 == 0 or n3 == 0 or n5 == 0 or n7 == 0:
        return True
    return False


# The middle point has the highest grayness
def localmaximum(n0, n1, n2, n3, n4, n5, n6, n7, n8):
    if n0 > n1 and n0 > n2 and n0 > n3 and n0 > n4 and n0 > n5 and n0 > n6 and n0 > n7 and n0 > n8:
        return True
    return False


# Checks if it is an end point
def endpoint(img, row, col):
    array = []
    array.extend([img[row - 1][col], img[row][col - 1], img[row + 1][col], img[row][col + 1]])

    if np.count_nonzero(array) == 1:
        del array[:]

        if img[row - 1][col] != 0:
            array.extend([img[row - 2][col], img[row - 1][col - 1], img[row - 1][col + 1]])

            if np.count_nonzero(array) == 1:
                return True

        if img[row][col - 1] != 0:
            array.extend([img[row - 1][col - 1], img[row][col - 2], img[row + 1][col - 1]])

            if np.count_nonzero(array) == 1:
                return True

        if img[row + 1][col] != 0:
            array.extend([img[row + 1][col - 1], img[row + 2][col], img[row + 1][col + 1]])

            if np.count_nonzero(array) == 1:
                return True

        if img[row][col + 1] != 0:
            array.extend([img[row - 1][col + 1], img[row][col + 2], img[row + 1][col + 1]])

            if np.count_nonzero(array) == 1:
                return True

    return False


# Returns True if the point can be deleted so the path is not weakened in the corner
def connectedcorner(img, row, col):
    num = 0
    if min(img[row][col + 1], img[row - 1][col]) == 0 or img[row - 1][col + 1] >= img[row][col]:
        num += 1
    if min(img[row - 1][col], img[row][col - 1]) == 0 or img[row - 1][col - 1] >= img[row][col]:
        num += 1
    if min(img[row][col - 1], img[row + 1][col]) == 0 or img[row + 1][col - 1] >= img[row][col]:
        num += 1
    if min(img[row + 1][col], img[row][col + 1]) == 0 or img[row + 1][col + 1] >= img[row][col]:
        num += 1
    if num == 4:
        return True
    return False


# Returns True if the point can be deleted so tha path is not weakened
def connectedpath(img, row, col):
    if min(img[row][col + 1], img[row][col - 1]) > 0:
        if img[row + 1][col] < img[row][col] and img[row - 1][col] < img[row][col]:
            return False
    if min(img[row - 1][col], img[row + 1][col]) > 0:
        if img[row][col - 1] < img[row][col] and img[row][col + 1] < img[row][col]:
            return False
    return True


# Returns the maximum neighbours value in the 3x3 neighbourhood
def dilation(img, row, col):
    x = int(img[row][col])
    if int(img[row][col + 1]) > x:
        x = int(img[row][col + 1])
    if int(img[row - 1][col + 1]) > x:
        x = int(img[row - 1][col + 1])
    if int(img[row - 1][col]) > x:
        x = int(img[row - 1][col])
    if int(img[row - 1][col - 1]) > x:
        x = int(img[row - 1][col - 1])
    if int(img[row][col - 1]) > x:
        x = int(img[row][col - 1])
    if int(img[row + 1][col - 1]) > x:
        x = int(img[row + 1][col - 1])
    if int(img[row + 1][col]) > x:
        x = int(img[row + 1][col])
    if int(img[row + 1][col + 1]) > x:
        x = int(img[row + 1][col + 1])
    return x


# Returns the minimum neighbours value in the 3x3 neighbourhood
def erosion(img, row, col):
    x = int(img[row][col])
    if int(img[row][col + 1]) < x:
        x = int(img[row][col + 1])
    if int(img[row - 1][col + 1]) < x:
        x = int(img[row - 1][col + 1])
    if int(img[row - 1][col]) < x:
        x = int(img[row - 1][col])
    if int(img[row - 1][col - 1]) < x:
        x = int(img[row - 1][col - 1])
    if int(img[row][col - 1]) < x:
        x = int(img[row][col - 1])
    if int(img[row + 1][col - 1]) < x:
        x = int(img[row + 1][col - 1])
    if int(img[row + 1][col]) < x:
        x = int(img[row + 1][col])
    if int(img[row + 1][col + 1]) < x:
        x = int(img[row + 1][col + 1])
    return x


# Returns the maximum value in the 5x5 neighbourhood
def dilationfar(img, row, col):
    x = dilation(img, row, col)
    if int(img[row][col + 2]) > x:
        x = int(img[row][col + 2])
    if int(img[row - 1][col + 2]) > x:
        x = int(img[row - 1][col + 2])
    if int(img[row - 2][col + 2]) > x:
        x = int(img[row - 2][col + 2])
    if int(img[row - 2][col + 1]) > x:
        x = int(img[row - 2][col + 1])
    if int(img[row - 2][col]) > x:
        x = int(img[row - 2][col])
    if int(img[row - 2][col - 1]) > x:
        x = int(img[row - 2][col - 1])
    if int(img[row - 2][col - 2]) > x:
        x = int(img[row - 2][col - 2])
    if int(img[row - 1][col - 2]) > x:
        x = int(img[row - 1][col - 2])
    if int(img[row][col - 2]) > x:
        x = int(img[row][col - 2])
    if int(img[row + 1][col - 2]) > x:
        x = int(img[row + 1][col - 2])
    if int(img[row + 2][col - 2]) > x:
        x = int(img[row + 2][col - 2])
    if int(img[row + 2][col - 1]) > x:
        x = int(img[row + 2][col - 1])
    if int(img[row + 2][col]) > x:
        x = int(img[row + 2][col])
    if int(img[row + 2][col + 1]) > x:
        x = int(img[row + 2][col + 1])
    if int(img[row + 2][col + 2]) > x:
        x = int(img[row + 2][col + 2])
    if int(img[row + 1][col + 2]) > x:
        x = int(img[row + 1][col + 2])
    return x


# Returns the minimum value in the 5x5 neighbourhood
def erosionfar(img, row, col):
    x = erosion(img, row, col)
    if int(img[row][col + 2]) < x:
        x = int(img[row][col + 2])
    if int(img[row - 1][col + 2]) < x:
        x = int(img[row - 1][col + 2])
    if int(img[row - 2][col + 2]) < x:
        x = int(img[row - 2][col + 2])
    if int(img[row - 2][col + 1]) < x:
        x = int(img[row - 2][col + 1])
    if int(img[row - 2][col]) < x:
        x = int(img[row - 2][col])
    if int(img[row - 2][col - 1]) < x:
        x = int(img[row - 2][col - 1])
    if int(img[row - 2][col - 2]) < x:
        x = int(img[row - 2][col - 2])
    if int(img[row - 1][col - 2]) < x:
        x = int(img[row - 1][col - 2])
    if int(img[row][col - 2]) < x:
        x = int(img[row][col - 2])
    if int(img[row + 1][col - 2]) < x:
        x = int(img[row + 1][col - 2])
    if int(img[row + 2][col - 2]) < x:
        x = int(img[row + 2][col - 2])
    if int(img[row + 2][col - 1]) < x:
        x = int(img[row + 2][col - 1])
    if int(img[row + 2][col]) < x:
        x = int(img[row + 2][col])
    if int(img[row + 2][col + 1]) < x:
        x = int(img[row + 2][col + 1])
    if int(img[row + 2][col + 2]) < x:
        x = int(img[row + 2][col + 2])
    if int(img[row + 1][col + 2]) < x:
        x = int(img[row + 1][col + 2])
    return x


# Count the value differences in the 8 neighbourhood
def countf(img, row, col):
    if img[row][col + 1] < img[row][col] and (img[row][col + 1] < img[row - 1][col + 1] or img[row][col + 1] < img[row - 1][col]):
        f1 = -1
    elif img[row][col + 1] > img[row - 1][col] and img[row - 1][col] < img[row][col]:
        f1 = 1
    else:
        f1 = 0
    if img[row - 1][col] < img[row][col] and (img[row - 1][col] < img[row - 1][col - 1] or img[row - 1][col] < img[row][col - 1]):
        f3 = -1
    elif img[row - 1][col] > img[row][col - 1] and img[row][col - 1] < img[row][col]:
        f3 = 1
    else:
        f3 = 0
    if img[row][col - 1] < img[row][col] and (img[row][col - 1] < img[row + 1][col - 1] or img[row][col - 1] < img[row + 1][col]):
        f5 = -1
    elif img[row][col - 1] > img[row + 1][col] and img[row + 1][col] < img[row][col]:
        f5 = 1
    else:
        f5 = 0
    if img[row + 1][col] < img[row][col] and (img[row + 1][col] < img[row + 1][col + 1] or img[row + 1][col] < img[row][col + 1]):
        f7 = -1
    elif img[row + 1][col] > img[row][col + 1] and img[row][col + 1] < img[row][col]:
        f7 = 1
    else:
        f7 = 0
    if img[row - 1][col + 1] > img[row - 1][col] and img[row - 1][col] < img[row][col]:
        f2 = 1
    else:
        f2 = 0
    if img[row - 1][col - 1] > img[row][col - 1] and img[row][col - 1] < img[row][col]:
        f4 = 1
    else:
        f4 = 0
    if img[row + 1][col - 1] > img[row + 1][col] and img[row + 1][col] < img[row][col]:
        f6 = 1
    else:
        f6 = 0
    if img[row + 1][col + 1] > img[row][col + 1] and img[row][col + 1] < img[row][col]:
        f8 = 1
    else:
        f8 = 0
    X = [f1, f2, f3, f4, f5, f6, f7, f8, f1]
    last_sign = 0
    sign_changes = 0

    for x in X:
        if x == 0:
            continue
        elif x == 1:
            if last_sign == -1:
                sign_changes += 1
        last_sign = x

    return sign_changes
